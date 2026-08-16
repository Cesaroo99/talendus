"""Erreurs d'intégrations externes — jamais de secrets dans le message."""

from app.errors import AppError

CODES = {
    "INTEGRATION_NOT_CONFIGURED": 503,
    "INTEGRATION_DISABLED": 503,
    "INTEGRATION_NOT_IMPLEMENTED": 501,
    "INTEGRATION_AUTH": 502,
    "INTEGRATION_FORBIDDEN": 403,
    "INTEGRATION_INVALID_REQUEST": 400,
    "INTEGRATION_NOT_FOUND": 404,
    "INTEGRATION_RATE_LIMITED": 429,
    "INTEGRATION_TIMEOUT": 504,
    "INTEGRATION_UNAVAILABLE": 503,
    "INTEGRATION_PROVIDER_ERROR": 502,
    "INTEGRATION_INTERNAL": 500,
    "INTEGRATION_SIGNATURE_INVALID": 400,
    "INTEGRATION_DUPLICATE": 200,
}


class IntegrationError(AppError):
    def __init__(
        self,
        message: str,
        code: str,
        *,
        provider: str | None = None,
        status_code: int | None = None,
        details: list | None = None,
    ):
        http_status = status_code or CODES.get(code, 502)
        super().__init__(http_status, message, code, details)
        self.provider = provider


def map_http_error(status_code: int, provider: str, operation: str) -> IntegrationError:
    if status_code in {401, 403}:
        code = "INTEGRATION_AUTH" if status_code == 401 else "INTEGRATION_FORBIDDEN"
        return IntegrationError(
            f"{provider} a refusé l'opération {operation}.",
            code,
            provider=provider,
            status_code=502 if status_code == 401 else 403,
        )
    if status_code == 404:
        return IntegrationError(f"Ressource {provider} introuvable.", "INTEGRATION_NOT_FOUND", provider=provider)
    if status_code == 429:
        return IntegrationError(f"{provider} a limité le débit.", "INTEGRATION_RATE_LIMITED", provider=provider)
    if status_code in {408, 504}:
        return IntegrationError(f"{provider} n'a pas répondu à temps.", "INTEGRATION_TIMEOUT", provider=provider)
    if status_code >= 500:
        return IntegrationError(
            f"{provider} est temporairement indisponible.",
            "INTEGRATION_UNAVAILABLE",
            provider=provider,
        )
    return IntegrationError(
        f"{provider} a renvoyé une erreur ({operation}).",
        "INTEGRATION_PROVIDER_ERROR",
        provider=provider,
    )
