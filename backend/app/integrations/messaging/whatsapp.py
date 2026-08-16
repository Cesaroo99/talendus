"""WhatsApp Business Cloud API — messages transactionnels uniquement."""

from __future__ import annotations

from app.config import get_settings
from app.integrations import http
from app.integrations.errors import IntegrationError
from app.integrations.registry import require_active

TEMPLATES = {
    "application_confirm": "application_confirm",
    "application_status": "application_status",
    "interview_invite": "interview_invite",
    "interview_reminder": "interview_reminder",
    "candidate_notice": "candidate_notice",
    "employer_notice": "employer_notice",
}


class WhatsAppService:
    name = "whatsapp"

    def send(
        self,
        *,
        recipient: str,
        template: str,
        variables: dict | None = None,
        message_type: str = "template",
    ) -> dict:
        if template not in TEMPLATES:
            raise IntegrationError(
                "Modèle WhatsApp inconnu.",
                "INTEGRATION_INVALID_REQUEST",
                provider=self.name,
                details=[{"field": "template", "message": "Modèle non reconnu."}],
            )
        if not recipient or not recipient.strip():
            raise IntegrationError(
                "Destinataire WhatsApp manquant.",
                "INTEGRATION_INVALID_REQUEST",
                provider=self.name,
            )
        require_active(self.name)
        settings = get_settings()
        url = f"{settings.whatsapp_api_base_url.rstrip('/')}/{settings.whatsapp_phone_number_id}/messages"
        components = []
        if variables:
            components.append(
                {
                    "type": "body",
                    "parameters": [{"type": "text", "text": str(v)} for v in variables.values()],
                }
            )
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient.strip(),
            "type": message_type,
            "template": {"name": TEMPLATES[template], "language": {"code": "fr"}, "components": components},
        }
        response = http.request(
            "POST",
            url,
            provider=self.name,
            operation=f"send.{template}",
            headers={"Authorization": f"Bearer {settings.whatsapp_access_token}", "Content-Type": "application/json"},
            json=payload,
        )
        data = response.json()
        message_id = None
        messages = data.get("messages") or []
        if messages:
            message_id = messages[0].get("id")
        return {
            "provider": self.name,
            "status": "queued",
            "template": template,
            "message_id": message_id,
            "recipient": recipient.strip()[-4:].rjust(len(recipient.strip()), "*"),
        }
