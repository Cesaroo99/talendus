"""Catalogue des fournisseurs : prepared / configured / active — jamais de secrets."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.config import get_settings
from app.integrations.errors import IntegrationError


@dataclass(frozen=True)
class ProviderSpec:
    name: str
    category: str
    label: str
    env_vars: tuple[str, ...]
    optional_env: tuple[str, ...] = ()
    description: str = ""
    implemented: bool = False
    notes: str = ""
    extra: dict = field(default_factory=dict, hash=False, compare=False)


def _secret(name: str) -> str:
    return (getattr(get_settings(), name, "") or "").strip()


def _flag(name: str) -> bool:
    return bool(getattr(get_settings(), name, False))


def _has_all(names: tuple[str, ...]) -> bool:
    return all(_secret(n) for n in names)


PROVIDERS: tuple[ProviderSpec, ...] = (
    ProviderSpec(
        name="email",
        category="messaging",
        label="E-mail SMTP",
        env_vars=("email_username", "email_password"),
        optional_env=("email_server", "email_from"),
        description="File d’e-mails persistée. Expéditeur info@talendus.ca. Envoi réel si SMTP est activé (admin → Paramètres → Courriel, ou EMAIL_ENABLED=true).",
        implemented=True,
        notes="Réglages SMTP aussi dans l’admin (Paramètres → Courriel).",
    ),
    ProviderSpec(
        name="s3",
        category="storage",
        label="Stockage S3",
        env_vars=("s3_bucket",),
        optional_env=("s3_access_key", "s3_secret_key", "s3_region", "s3_endpoint_url", "s3_prefix"),
        description="Upload CV vers S3 si STORAGE_BACKEND=s3.",
        implemented=True,
        notes="Déjà branché via app.services.storage.",
    ),
    ProviderSpec(
        name="stripe",
        category="payments",
        label="Stripe Checkout",
        env_vars=("stripe_secret_key",),
        optional_env=("stripe_webhook_secret", "stripe_publishable_key"),
        description="Checkout et webhook. Jamais de données bancaires en base Talendus.",
        implemented=True,
        notes="POST /api/invoices/{id}/checkout et POST /api/webhooks/stripe.",
    ),
    ProviderSpec(
        name="paypal",
        category="payments",
        label="PayPal",
        env_vars=("paypal_client_id", "paypal_client_secret"),
        optional_env=("paypal_webhook_id", "paypal_api_base_url"),
        description="Abstraction PaymentService. Orders API uniquement avec identifiants.",
        implemented=True,
        notes="Préparée : 503 sans clés. Appel HTTP officiel si configurée.",
    ),
    ProviderSpec(
        name="linkedin",
        category="jobs",
        label="LinkedIn Jobs",
        env_vars=("linkedin_client_id", "linkedin_client_secret"),
        optional_env=("linkedin_api_base_url",),
        description="Partage d'URL toujours disponible. Ingest d'offres via API partenaire seulement.",
        implemented=False,
        notes="Pas de scraping. L'import d'offres exige un accès partenaire LinkedIn.",
    ),
    ProviderSpec(
        name="indeed",
        category="jobs",
        label="Indeed",
        env_vars=("indeed_api_key",),
        optional_env=("indeed_publisher_id", "indeed_api_base_url"),
        description="Import d'offres via API / flux officiels uniquement.",
        implemented=False,
        notes="Pas de scraping. Compte partenaire Indeed requis.",
    ),
    ProviderSpec(
        name="whatsapp",
        category="messaging",
        label="WhatsApp Business",
        env_vars=("whatsapp_access_token", "whatsapp_phone_number_id"),
        optional_env=("whatsapp_webhook_secret", "whatsapp_api_base_url"),
        description="Messages transactionnels (templates Cloud API).",
        implemented=True,
        notes="Envoi réel seulement si token + phone_number_id. Webhook GET/POST /api/webhooks/whatsapp.",
    ),
    ProviderSpec(
        name="google_maps",
        category="maps",
        label="Google Maps",
        env_vars=("google_maps_api_key",),
        optional_env=("google_maps_api_base_url",),
        description="Géocodage et recherche d'adresses.",
        implemented=True,
        notes="Appel Geocoding API seulement si GOOGLE_MAPS_API_KEY est défini.",
    ),
    ProviderSpec(
        name="openai",
        category="ai",
        label="OpenAI",
        env_vars=("openai_api_key",),
        optional_env=("openai_model", "openai_api_base_url"),
        description="Analyse CV, suggestions — jamais appelée automatiquement.",
        implemented=True,
        notes="Uniquement via POST /api/integrations/ai/complete (staff). Clé jamais au front.",
    ),
    ProviderSpec(
        name="esignature",
        category="esignature",
        label="Signature électronique",
        env_vars=("esignature_api_key",),
        optional_env=("esignature_api_base_url", "esignature_webhook_secret", "esignature_provider"),
        description="Enveloppes, signataires, webhooks. La signature interne SHA-256 reste distincte.",
        implemented=False,
        notes="Interface prête. Fournisseur (DocuSign / autre) à brancher avec un compte API.",
    ),
    ProviderSpec(
        name="google_login",
        category="auth",
        label="Connexion Google",
        env_vars=("google_oauth_client_id",),
        description="Bouton Continuer avec Google. Sans identifiant, la connexion se fait par courriel.",
        implemented=True,
        notes="GOOGLE_OAUTH_CLIENT_ID dans Render. Aucun secret n'est envoyé au navigateur au-delà de cet identifiant public.",
    ),
    ProviderSpec(
        name="linkedin_login",
        category="auth",
        label="Connexion LinkedIn",
        env_vars=("linkedin_oauth_client_id",),
        description="Connexion LinkedIn, distincte de l'import d'offres.",
        implemented=True,
        notes="LINKEDIN_OAUTH_CLIENT_ID. Le bouton n'apparaît que si cet identifiant est présent.",
    ),
)


def _enabled(name: str) -> bool:
    settings = get_settings()
    mapping = {
        "email": settings.email_enabled,
        "s3": (settings.storage_backend or "local").lower() == "s3",
        "stripe": settings.stripe_enabled,
        "paypal": settings.paypal_enabled,
        "linkedin": settings.linkedin_enabled,
        "indeed": settings.indeed_enabled,
        "whatsapp": settings.whatsapp_enabled,
        "google_maps": settings.google_maps_enabled,
        "openai": settings.openai_enabled,
        "esignature": settings.esignature_enabled,
        "google_login": bool(settings.google_oauth_client_id),
        "linkedin_login": bool(settings.linkedin_oauth_client_id),
    }
    return bool(mapping.get(name, False))


def _configured(spec: ProviderSpec) -> bool:
    if spec.name == "email":
        return bool(get_settings().email_enabled)
    if spec.name == "s3":
        return (get_settings().storage_backend or "").lower() == "s3" and bool(get_settings().s3_bucket)
    if spec.name == "indeed":
        return bool(_secret("indeed_api_key") or _secret("indeed_publisher_id"))
    if spec.name == "google_login":
        return bool(_secret("google_oauth_client_id"))
    if spec.name == "linkedin_login":
        return bool(_secret("linkedin_oauth_client_id"))
    return _has_all(spec.env_vars)


def _state(spec: ProviderSpec) -> str:
    configured = _configured(spec)
    enabled = _enabled(spec.name)
    if spec.name in {"email", "s3", "google_login", "linkedin_login"}:
        return "active" if configured else "prepared"
    if spec.name == "stripe":
        if configured and enabled:
            return "active"
        if configured:
            return "configured"
        return "prepared"
    if configured and enabled and spec.implemented:
        return "active"
    if configured:
        return "configured"
    return "prepared"


def provider_status(name: str) -> dict:
    spec = next((p for p in PROVIDERS if p.name == name), None)
    if spec is None:
        raise IntegrationError("Fournisseur inconnu.", "INTEGRATION_NOT_FOUND", provider=name)
    configured = _configured(spec)
    enabled = _enabled(spec.name)
    state = _state(spec)
    env_names = [n.upper() for n in spec.env_vars] + [n.upper() for n in spec.optional_env]
    message = {
        "active": f"{spec.label} est actif.",
        "configured": f"{spec.label} a des identifiants mais n'est pas activé (ou l'API partenaire n'est pas branchée).",
        "prepared": f"{spec.label} est préparé, sans identifiants. Aucun appel externe n'est effectué.",
    }[state]
    if state == "configured" and not spec.implemented:
        message = f"{spec.label} a des identifiants mais l'API partenaire n'est pas encore branchée (pas d'appel simulé)."
    return {
        "name": spec.name,
        "label": spec.label,
        "category": spec.category,
        "enabled": enabled,
        "configured": configured,
        "implemented": spec.implemented,
        "state": state,
        "description": spec.description,
        "notes": spec.notes,
        "env_vars": env_names,
        "message": message,
    }


def catalog() -> list[dict]:
    return [provider_status(p.name) for p in PROVIDERS]


def is_active(name: str) -> bool:
    try:
        return provider_status(name)["state"] == "active"
    except IntegrationError:
        return False


def require_configured(name: str) -> dict:
    status = provider_status(name)
    if not status["configured"]:
        raise IntegrationError(
            f"{status['label']} n'est pas configuré (identifiants manquants).",
            "INTEGRATION_NOT_CONFIGURED",
            provider=name,
        )
    return status


def require_active(name: str) -> dict:
    status = require_configured(name)
    if not status["enabled"] and name not in {"email", "s3", "google_login", "linkedin_login"}:
        raise IntegrationError(
            f"{status['label']} est désactivé.",
            "INTEGRATION_DISABLED",
            provider=name,
        )
    if not status["implemented"]:
        raise IntegrationError(
            f"{status['label']} n'appelle aucune API tant qu'un accès partenaire officiel n'est pas branché.",
            "INTEGRATION_NOT_IMPLEMENTED",
            provider=name,
        )
    return status
