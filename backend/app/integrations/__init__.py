"""Couche d'intégrations externes Talendus — un module par fournisseur."""

from app.integrations.registry import catalog, provider_status, require_active, require_configured

__all__ = ["catalog", "provider_status", "require_active", "require_configured"]
