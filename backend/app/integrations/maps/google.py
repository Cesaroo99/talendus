"""Google Maps Geocoding — clé uniquement côté serveur."""

from __future__ import annotations

from app.config import get_settings
from app.integrations import http
from app.integrations.errors import IntegrationError
from app.integrations.registry import require_active


class GoogleMapsService:
    name = "google_maps"

    def geocode(self, address: str) -> dict:
        if not address or not address.strip():
            raise IntegrationError(
                "Adresse manquante.",
                "INTEGRATION_INVALID_REQUEST",
                provider=self.name,
            )
        require_active(self.name)
        settings = get_settings()
        response = http.request(
            "GET",
            f"{settings.google_maps_api_base_url.rstrip('/')}/geocode/json",
            provider=self.name,
            operation="geocode",
            params={"address": address.strip(), "key": settings.google_maps_api_key, "region": "ca"},
        )
        data = response.json() or {}
        status = data.get("status")
        if status == "ZERO_RESULTS":
            raise IntegrationError("Adresse introuvable.", "INTEGRATION_NOT_FOUND", provider=self.name)
        if status == "OVER_QUERY_LIMIT":
            raise IntegrationError("Limite Google Maps atteinte.", "INTEGRATION_RATE_LIMITED", provider=self.name)
        if status == "REQUEST_DENIED":
            raise IntegrationError("Google Maps a refusé la requête.", "INTEGRATION_AUTH", provider=self.name)
        if status not in {None, "OK"}:
            raise IntegrationError("Géocodage Google Maps impossible.", "INTEGRATION_PROVIDER_ERROR", provider=self.name)
        results = data.get("results") or []
        if not results:
            raise IntegrationError("Adresse introuvable.", "INTEGRATION_NOT_FOUND", provider=self.name)
        first = results[0]
        loc = ((first.get("geometry") or {}).get("location")) or {}
        return {
            "formatted_address": first.get("formatted_address"),
            "lat": loc.get("lat"),
            "lng": loc.get("lng"),
            "place_id": first.get("place_id"),
            "types": first.get("types") or [],
        }

    def distance(self, origin: str, destination: str) -> dict:
        if not origin or not destination:
            raise IntegrationError("Origine et destination requises.", "INTEGRATION_INVALID_REQUEST", provider=self.name)
        require_active(self.name)
        settings = get_settings()
        response = http.request(
            "GET",
            f"{settings.google_maps_api_base_url.rstrip('/')}/distancematrix/json",
            provider=self.name,
            operation="distance",
            params={
                "origins": origin,
                "destinations": destination,
                "key": settings.google_maps_api_key,
                "units": "metric",
                "region": "ca",
            },
        )
        data = response.json() or {}
        rows = data.get("rows") or []
        element = ((rows[0].get("elements") or [{}])[0] if rows else {})
        return {
            "origin": origin,
            "destination": destination,
            "distance_m": (element.get("distance") or {}).get("value"),
            "duration_s": (element.get("duration") or {}).get("value"),
            "status": element.get("status") or data.get("status"),
        }
