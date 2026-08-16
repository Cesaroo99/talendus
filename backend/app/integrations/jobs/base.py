from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class ExternalJobPayload:
    external_id: str
    source: str
    title: str
    company: str | None = None
    description: str | None = None
    location: str | None = None
    salary: str | None = None
    employment_type: str | None = None
    original_url: str | None = None
    published_at: str | None = None
    extra: dict = field(default_factory=dict)


class JobBoardProvider(Protocol):
    name: str

    def fetch_jobs(self, query: str | None = None) -> list[ExternalJobPayload]: ...
