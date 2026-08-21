from __future__ import annotations

import time
from collections import defaultdict, deque

from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse, Response

from app.config import get_settings
from app.deps import client_ip
from app.errors import error_body
from app.services.seo import PRIVATE_PATHS, REDIRECTS

CSP = (
    "default-src 'self'; "
    "base-uri 'self'; "
    "form-action 'self' mailto: tel: https://wa.me; "
    "object-src 'none'; "
    "frame-ancestors 'none'; "
    "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.google-analytics.com "
    "https://connect.facebook.net https://accounts.google.com https://js.stripe.com; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com data:; "
    "img-src 'self' data: blob: https:; "
    "media-src 'self' blob:; "
    "connect-src 'self' https: wss:; "
    "frame-src 'self' https://js.stripe.com https://accounts.google.com https://www.google.com; "
    "worker-src 'self'; "
    "upgrade-insecure-requests"
)
SPAM_PATHS = {
    "/api/contact",
    "/api/auth/register",
    "/api/auth/login",
    "/api/auth/forgot-password",
    "/api/applications/public",
    "/api/talent-profile",
}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
        except StarletteHTTPException:
            raise
        except Exception:
            from app.errors import html_error, wants_html

            if wants_html(request):
                return html_error(503)
            return JSONResponse(
                status_code=503,
                content=error_body("Service momentanément indisponible.", "UNAVAILABLE"),
            )
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault("X-XSS-Protection", "1; mode=block")
        response.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(self), camera=(self)")
        response.headers.setdefault("Content-Security-Policy", CSP)
        path = request.url.path
        if path.startswith("/api/"):
            response.headers.setdefault("Cache-Control", "no-store")
        if get_settings().app_env == "production":
            response.headers.setdefault("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
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
            "/api/ready",
            "/api/docs",
            "/api/redoc",
            "/api/openapi.json",
            "/api/tracking/config",
            "/api/services",
        }:
            return await call_next(request)
        if request.url.path.startswith("/api/webhooks/"):
            return await call_next(request)
        ip = client_ip(request) or "unknown"
        now = time.time()
        window = self.hits[ip]
        while window and now - window[0] > 60:
            window.popleft()
        cap = self.limit
        path = request.url.path.rstrip("/")
        if path in SPAM_PATHS and get_settings().app_env != "test":
            cap = min(self.limit, 20)
        if len(window) >= cap:
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
