"""État public et interne des services connexes — aucun secret."""

from __future__ import annotations

from app.config import get_settings
from app.integrations.registry import catalog, is_active, provider_status
from app.services.seo import tracking_public_config

DEMO_PHONES = {"15145550199", "5145550199", "15550199"}

NEXT_STEPS = {
    "email": {
        "prepared": "Dans Render, ajoutez le serveur d'envoi (EMAIL_SERVER, EMAIL_USERNAME, EMAIL_PASSWORD) puis passez EMAIL_ENABLED à true. Tant que ce n'est pas fait, les messages restent dans Talendus.",
        "active": "Les courriels partent vraiment.",
    },
    "s3": {
        "prepared": "Les CV sont sur le disque Talendus. Un bucket S3 n'est utile que si vous voulez une copie hors serveur.",
        "active": "Les fichiers partent vers S3.",
    },
    "stripe": {
        "prepared": "Le règlement par virement reste le mode par défaut. Pour la carte, ajoutez STRIPE_SECRET_KEY et STRIPE_WEBHOOK_SECRET, puis STRIPE_ENABLED=true.",
        "configured": "Les clés Stripe sont là. Passez STRIPE_ENABLED=true pour afficher le bouton carte aux entreprises.",
        "active": "Les entreprises peuvent payer une facture par carte.",
    },
    "paypal": {
        "prepared": "Inutile tant que le virement suffit. Sinon : PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET et PAYPAL_ENABLED=true.",
        "active": "Le bouton PayPal s'affiche sur les factures.",
    },
    "google_login": {
        "prepared": "La connexion se fait par courriel. Pour « Continuer avec Google », créez un identifiant OAuth dans Google Cloud et mettez GOOGLE_OAUTH_CLIENT_ID dans Render.",
        "active": "Le bouton Google s'affiche à la connexion.",
    },
    "linkedin_login": {
        "prepared": "Optionnel. LinkedIn Login exige un identifiant d'application LinkedIn (LINKEDIN_OAUTH_CLIENT_ID).",
        "active": "La connexion LinkedIn est prête côté serveur.",
    },
    "linkedin": {
        "prepared": "Le partage d'une offre par lien LinkedIn fonctionne déjà. L'import automatique d'offres exige un accès partenaire LinkedIn — pas du scraping.",
        "configured": "Identifiants présents, mais l'import d'offres LinkedIn n'est pas branché (accès partenaire requis).",
    },
    "indeed": {
        "prepared": "Même logique que LinkedIn : pas d'import tant qu'Indeed n'a pas ouvert un accès partenaire.",
    },
    "whatsapp": {
        "prepared": "Le bouton WhatsApp du site ouvre une conversation vers le numéro affiché. Les messages automatiques (candidature, entretien) exigent WhatsApp Business : WHATSAPP_ACCESS_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_ENABLED=true.",
        "active": "Les messages automatiques WhatsApp peuvent partir.",
    },
    "google_maps": {
        "prepared": "La carte de contact fonctionne. Le calcul de distance autour d'une ville exige GOOGLE_MAPS_API_KEY et GOOGLE_MAPS_ENABLED=true.",
        "active": "Le géocodage des adresses est actif.",
    },
    "openai": {
        "prepared": "L'IA interne de Talendus n'appelle pas OpenAI toute seule. Une clé OPENAI_API_KEY + OPENAI_ENABLED=true sert seulement à une analyse explicite par l'équipe.",
        "active": "L'analyse assistée (bouton équipe) peut appeler OpenAI.",
    },
    "esignature": {
        "prepared": "Les mandats se signent déjà dans l'espace entreprise. DocuSign n'est utile que si un client l'exige.",
        "configured": "Clé présente, mais le fournisseur de signature tierce n'est pas branché. La signature dans Talendus reste disponible.",
    },
}


def _digits(value: str) -> str:
    return "".join(ch for ch in (value or "") if ch.isdigit())


def _canada_e164(value: str) -> str:
    digits = _digits(value)
    if len(digits) == 10:
        return "1" + digits
    return digits


def public_services() -> dict:
    settings = get_settings()
    phone_e164 = _canada_e164(settings.public_phone_e164)
    phone_display = (settings.public_phone_display or "").strip()
    email = (settings.public_email or "").strip() or "info@talendus.ca"
    demo = (not phone_e164) or phone_e164 in DEMO_PHONES
    if demo:
        phone_e164 = ""
        phone_display = ""
    tracking = tracking_public_config()
    email_sending = bool(settings.email_enabled)
    try:
        from app.database import SessionLocal
        from app.services.email import runtime_email_config

        db = SessionLocal()
        try:
            email_sending = bool(runtime_email_config(db).enabled)
        finally:
            db.close()
    except Exception:  # noqa: BLE001
        pass
    return {
        "contact": {
            "phone_e164": phone_e164,
            "phone_display": phone_display,
            "email": email,
            "whatsapp_e164": "" if demo else phone_e164,
            "demo": demo,
        },
        "payments": {
            "transfer": True,
            "card": is_active("stripe"),
            "paypal": is_active("paypal"),
        },
        "login": {
            "password": True,
            "google": bool(settings.google_oauth_client_id),
            "linkedin": bool(
                settings.linkedin_oauth_client_id
                and (settings.linkedin_oauth_client_secret or settings.linkedin_client_secret)
            ),
        },
        "messaging": {
            "in_app": True,
            "email_sending": email_sending,
            "whatsapp_api": is_active("whatsapp"),
            "sms": False,
            "push": False,
        },
        "maps": is_active("google_maps"),
        "tracking": bool(tracking.get("enabled")),
    }


def _todos(services: dict, providers: list[dict]) -> list[dict]:
    todos: list[dict] = []
    if services["contact"]["demo"]:
        todos.append(
            {
                "id": "phone",
                "priority": 1,
                "title": "Mettre le vrai numéro de téléphone",
                "detail": "Le site affiche encore 514 555-0199. Dans Render → Environment, ajoutez PUBLIC_PHONE_E164 (chiffres, ex. 15141234567) et PUBLIC_PHONE_DISPLAY (ex. 514 123-4567). Le site mettra à jour appels et WhatsApp tout seul.",
            }
        )
    email_row = next((p for p in providers if p["name"] == "email"), None)
    if not email_row or email_row["state"] != "active":
        todos.append(
            {
                "id": "email",
                "priority": 1,
                "title": "Activer l'envoi des courriels",
                "detail": "Les formulaires et alertes sont bien enregistrés dans Talendus, mais ils ne partent pas vers les boîtes courriel. Ajoutez EMAIL_SERVER, EMAIL_USERNAME, EMAIL_PASSWORD puis EMAIL_ENABLED=true.",
            }
        )
    if not services["login"]["google"]:
        todos.append(
            {
                "id": "google",
                "priority": 2,
                "title": "Connexion Google (facultatif)",
                "detail": "Sans ça, on se connecte par courriel. Pour le bouton Google : identifiant OAuth dans Google Cloud, puis GOOGLE_OAUTH_CLIENT_ID dans Render.",
            }
        )
    if not services["payments"]["card"] and not services["payments"]["paypal"]:
        todos.append(
            {
                "id": "payments",
                "priority": 3,
                "title": "Paiement par carte (facultatif)",
                "detail": "Aujourd'hui les entreprises règlent par virement ou chèque, et Talendus enregistre le paiement. Stripe ou PayPal ne sont utiles que si vous voulez un paiement en ligne.",
            }
        )
    if not services["messaging"]["whatsapp_api"]:
        todos.append(
            {
                "id": "whatsapp",
                "priority": 3,
                "title": "WhatsApp Business (facultatif)",
                "detail": "Le bouton WhatsApp du site ouvre déjà une conversation. Les confirmations automatiques (candidature, entretien) demandent un compte WhatsApp Business.",
            }
        )
    todos.sort(key=lambda item: item["priority"])
    return todos


def enrich_provider(row: dict) -> dict:
    hints = NEXT_STEPS.get(row["name"]) or {}
    row = dict(row)
    row["next_step"] = hints.get(row["state"]) or hints.get("prepared") or row.get("notes") or ""
    return row


def staff_overview() -> dict:
    providers = [enrich_provider(row) for row in catalog()]
    services = public_services()
    return {
        "services": services,
        "providers": providers,
        "todos": _todos(services, providers),
        "stripe": provider_status("stripe")["state"],
        "email": provider_status("email")["state"],
    }
