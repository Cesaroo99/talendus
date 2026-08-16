import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import FileResponse as StarletteFileResponse

from app.boot import assert_runtime_safe
from app.config import get_settings
from app.database import init_db
from app.errors import AppError, app_error_handler, http_error_handler, unhandled_handler, validation_handler
from app.middleware import RateLimitMiddleware, SecurityHeadersMiddleware, SeoRedirectMiddleware
from app.seed import seed_if_empty
from app.services.email import start_worker

settings = get_settings()
logger = logging.getLogger("talendus")
logging.basicConfig(level=logging.INFO if not settings.debug else logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(message)s")

SITE_ROOT = Path(__file__).resolve().parents[2]


class SiteStatic(StaticFiles):
    """404 HTML Talendus au lieu d'une erreur brute / 502 proxy."""

    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except StarletteHTTPException as exc:
            if exc.status_code == 404:
                not_found = SITE_ROOT / "404.html"
                if not_found.exists():
                    return StarletteFileResponse(not_found, status_code=404, media_type="text/html; charset=utf-8")
            raise


@asynccontextmanager
async def lifespan(_app: FastAPI):
    assert_runtime_safe(settings)
    try:
        init_db()
        if settings.app_env != "test":
            seed_if_empty()
            start_worker()
    except Exception:
        logger.exception("Démarrage base/seed en échec — le site public reste servi")
    logger.info("Talendus API ready env=%s", settings.app_env)
    yield


def create_app() -> FastAPI:
    public_docs = settings.app_env != "production"
    application = FastAPI(
        title="Talendus API",
        description="Back-end de la plateforme de recrutement industriel Talendus.",
        version="1.0.0",
        docs_url="/api/docs" if public_docs else None,
        redoc_url="/api/redoc" if public_docs else None,
        openapi_url="/api/openapi.json" if public_docs else None,
        lifespan=lifespan,
    )
    application.add_middleware(SecurityHeadersMiddleware)
    application.add_middleware(RateLimitMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list or ["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "Accept"],
    )
    application.add_middleware(SeoRedirectMiddleware)
    application.add_exception_handler(AppError, app_error_handler)
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, validation_handler)
    application.add_exception_handler(Exception, unhandled_handler)

    from app.api import (
        admin,
        alerts,
        applications,
        auth,
        blog,
        candidates,
        companies,
        contracts,
        documents,
        interviews,
        invoices,
        jobs,
        matching,
        messages,
        notifications,
        public,
        recruiters,
        site,
        users,
        webhooks,
        integrations,
    )

    application.include_router(public.router, prefix="/api")
    application.include_router(public.emails_router, prefix="/api")
    application.include_router(auth.router, prefix="/api")
    application.include_router(alerts.router, prefix="/api")
    application.include_router(users.router, prefix="/api")
    application.include_router(candidates.router, prefix="/api")
    application.include_router(companies.router, prefix="/api")
    application.include_router(recruiters.router, prefix="/api")
    application.include_router(jobs.router, prefix="/api")
    application.include_router(applications.router, prefix="/api")
    application.include_router(notifications.router, prefix="/api")
    application.include_router(messages.router, prefix="/api")
    application.include_router(documents.router, prefix="/api")
    application.include_router(interviews.router, prefix="/api")
    application.include_router(invoices.router, prefix="/api")
    application.include_router(contracts.router, prefix="/api")
    application.include_router(matching.router, prefix="/api")
    application.include_router(integrations.router, prefix="/api")
    application.include_router(blog.router, prefix="/api")
    application.include_router(blog.admin_router, prefix="/api")
    application.include_router(admin.router, prefix="/api")
    application.include_router(webhooks.router, prefix="/api")
    application.include_router(site.router)

    if SITE_ROOT.joinpath("index.html").exists() and settings.app_env != "test":
        application.mount("/", SiteStatic(directory=str(SITE_ROOT), html=True), name="site")
    return application


app = create_app()
