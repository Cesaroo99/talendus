"""Couche d'intégrations externes Talendus — un module par fournisseur."""

from app.integrations.registry import catalog, is_active, provider_status, require_active, require_configured

__all__ = ["catalog", "is_active", "provider_status", "require_active", "require_configured"]
