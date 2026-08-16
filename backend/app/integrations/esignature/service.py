"""Signature électronique tierce — distincte de la signature interne SHA-256."""

from __future__ import annotations

from app.integrations.errors import IntegrationError
from app.integrations.registry import require_active


class ESignatureService:
    name = "esignature"

    def create_document(self, *, title: str, file_url: str | None = None) -> dict:
        require_active(self.name)
        raise IntegrationError(
            "La création d'enveloppe exige un fournisseur de signature configuré (DocuSign ou équivalent).",
            "INTEGRATION_NOT_IMPLEMENTED",
            provider=self.name,
        )

    def add_signers(self, envelope_id: str, signers: list[dict]) -> dict:
        require_active(self.name)
        raise IntegrationError(
            "L'ajout de signataires n'est pas branché.",
            "INTEGRATION_NOT_IMPLEMENTED",
            provider=self.name,
        )

    def send(self, envelope_id: str) -> dict:
        require_active(self.name)
        raise IntegrationError("L'envoi pour signature n'est pas branché.", "INTEGRATION_NOT_IMPLEMENTED", provider=self.name)

    def status(self, envelope_id: str) -> dict:
        require_active(self.name)
        raise IntegrationError("Le statut d'enveloppe n'est pas branché.", "INTEGRATION_NOT_IMPLEMENTED", provider=self.name)

    def cancel(self, envelope_id: str) -> dict:
        require_active(self.name)
        raise IntegrationError("L'annulation d'enveloppe n'est pas branchée.", "INTEGRATION_NOT_IMPLEMENTED", provider=self.name)


def apply_esignature_event(db, payload: bytes) -> None:
    import json

    from sqlalchemy import select

    from app.models import Contract

    try:
        body = json.loads((payload or b"{}").decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return
    if not isinstance(body, dict):
        return
    envelope_id = body.get("envelopeId") or body.get("envelope_id") or body.get("id")
    status = body.get("status") or body.get("event")
    if not envelope_id:
        return
    row = db.scalar(select(Contract).where(Contract.esign_envelope_id == str(envelope_id)))
    if not row:
        return
    if status:
        row.esign_status = str(status)[:32]
    db.commit()
