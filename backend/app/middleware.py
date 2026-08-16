from __future__ import annotations

import time
from collections import defaultdict, deque

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, Response

from app.config import get_settings
from app.errors import error_body
from app.services.seo import PRIVATE_PATHS, REDIRECTS


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("X-XSS-Protection", "1; mode=block")
        response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        path = request.url.path
        if path.startswith("/api/"):
            response.headers.setdefault("Cache-Control", "no-store")
        private = (
            path.startswith("/admin")
            or path.startswith("/api/")
            or path.startswith("/candidate")
            or path.startswith("/employer")
            or path.startswith("/en/candidate")
            or path.startswith("/en/employer")
            or path in PRIVATE_PATHS
            or path.endswith("404.html")
            or response.status_code == 404
        )
        if private:
            response.headers["X-Robots-Tag"] = "noindex, nofollow"
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int | None = None):
        super().__init__(app)
        self.limit = limit or get_settings().rate_limit_per_minute
        self.hits: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next) -> Response:
        if not request.url.path.startswith("/api/"):
            return await call_next(request)
        if request.url.path.rstrip("/") in {
            "/api/health",
            "/api/docs",
            "/api/redoc",
            "/api/openapi.json",
            "/api/tracking/config",
        }:
            return await call_next(request)
        if request.url.path.startswith("/api/webhooks/"):
            return await call_next(request)
        ip = request.headers.get("x-forwarded-for", "").split(",")[0].strip() or (
            request.client.host if request.client else "unknown"
        )
        now = time.time()
        window = self.hits[ip]
        while window and now - window[0] > 60:
            window.popleft()
        if len(window) >= self.limit:
            return JSONResponse(
                status_code=429,
                content=error_body("Trop de requêtes. Réessayez dans une minute.", "RATE_LIMITED"),
            )
        window.append(now)
        return await call_next(request)


class SeoRedirectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        target = REDIRECTS.get(request.url.path)
        if target:
            return RedirectResponse(url=target, status_code=301)
        return await call_next(request)
