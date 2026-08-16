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
                        "content": "Tu assistes Talendus, agence de placement intelligente. Réponds en français, sans inventer de faits. L'IA aide les équipes Talendus dans leur processus interne ; elle n'est pas un moteur de matching en production : n'invente pas de scores ni de classements. L'entreprise ne cherche pas elle-même les candidats.",
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

    def analyze_resume(self, text: str) -> dict:
        return self.complete(purpose="resume_analysis", prompt=f"Analyse ce CV (recrutement, tous secteurs) :\n{text}")

    def extract_skills(self, text: str) -> dict:
        return self.complete(purpose="skill_extraction", prompt=f"Extrais les compétences, une par ligne :\n{text}")

    def classify_profile(self, text: str) -> dict:
        return self.complete(purpose="profile_classification", prompt=f"Classe ce profil (métier, niveau, secteur) :\n{text}")

    def improve_job_description(self, text: str) -> dict:
        return self.complete(purpose="job_description", prompt=f"Améliore cette description d'emploi sans inventer :\n{text}")

    def suggest_match(self, candidate_text: str, job_text: str) -> dict:
        return self.complete(
            purpose="matching_suggestion",
            prompt=f"Points de correspondance candidat/offre :\nCandidat:\n{candidate_text}\n\nOffre:\n{job_text}",
        )
