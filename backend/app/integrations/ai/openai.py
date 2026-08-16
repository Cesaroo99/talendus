"""OpenAI — jamais appelé automatiquement, clé exclusivement serveur."""

from __future__ import annotations

from app.config import get_settings
from app.integrations import http
from app.integrations.errors import IntegrationError
from app.integrations.registry import require_active

ALLOWED_PURPOSES = {
    "resume_analysis",
    "skill_extraction",
    "profile_classification",
    "job_description",
    "matching_suggestion",
    "recruiting_assist",
}


class OpenAIService:
    name = "openai"

    def complete(self, *, purpose: str, prompt: str, max_tokens: int = 400) -> dict:
        if purpose not in ALLOWED_PURPOSES:
            raise IntegrationError(
                "Usage OpenAI non autorisé.",
                "INTEGRATION_INVALID_REQUEST",
                provider=self.name,
            )
        if not prompt or not prompt.strip():
            raise IntegrationError("Prompt vide.", "INTEGRATION_INVALID_REQUEST", provider=self.name)
        require_active(self.name)
        settings = get_settings()
        response = http.request(
            "POST",
            f"{settings.openai_api_base_url.rstrip('/')}/chat/completions",
            provider=self.name,
            operation=purpose,
            headers={"Authorization": f"Bearer {settings.openai_api_key}", "Content-Type": "application/json"},
            json={
                "model": settings.openai_model,
                "max_tokens": min(max_tokens, 1200),
                "messages": [
                    {
                        "role": "system",
                        "content": "Tu assistes Talendus, cabinet de recrutement industriel au Québec. Réponds en français, sans inventer de faits.",
                    },
                    {"role": "user", "content": prompt.strip()[:8000]},
                ],
            },
        )
        data = response.json() or {}
        choice = (data.get("choices") or [{}])[0]
        text = ((choice.get("message") or {}).get("content")) or ""
        usage = data.get("usage") or {}
        return {
            "provider": self.name,
            "purpose": purpose,
            "text": text,
            "model": data.get("model") or settings.openai_model,
            "usage": {"prompt_tokens": usage.get("prompt_tokens"), "completion_tokens": usage.get("completion_tokens")},
        }
