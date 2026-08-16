"""Indeed — API / flux officiels uniquement, jamais de scraping."""

from app.integrations.errors import IntegrationError
from app.integrations.jobs.base import ExternalJobPayload, JobBoardProvider
from app.integrations.registry import require_active


class IndeedService:
    name = "indeed"

    def fetch_jobs(self, query: str | None = None) -> list[ExternalJobPayload]:
        require_active(self.name)
        raise IntegrationError(
            "L'import Indeed exige un accès API partenaire officiel. Aucun appel n'est simulé.",
            "INTEGRATION_NOT_IMPLEMENTED",
            provider=self.name,
        )


def service() -> JobBoardProvider:
    return IndeedService()
