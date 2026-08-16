import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import init_db
from app.errors import AppError, app_error_handler, http_error_handler, unhandled_handler, validation_handler
from app.middleware import RateLimitMiddleware, SecurityHeadersMiddleware
from app.seed import seed_if_empty
from app.services.email import start_worker

settings = get_settings()
logger = logging.getLogger("talendus")
logging.basicConfig(level=logging.INFO if not settings.debug else logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(message)s")

SITE_ROOT = Path(__file__).resolve().parents[2]


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    if settings.app_env != "test":
        seed_if_empty()
        start_worker()
    logger.info("Talendus API ready env=%s", settings.app_env)
    yield


def create_app() -> FastAPI:
    application = FastAPI(
        title="Talendus API",
        description="Back-end de la plateforme de recrutement industriel Talendus.",
        version="1.0.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
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
    application.add_exception_handler(AppError, app_error_handler)
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, validation_handler)
    application.add_exception_handler(Exception, unhandled_handler)

    from app.api import admin, applications, auth, candidates, companies, jobs, notifications, public, recruiters, users

    application.include_router(public.router, prefix="/api")
    application.include_router(public.emails_router, prefix="/api")
    application.include_router(auth.router, prefix="/api")
    application.include_router(users.router, prefix="/api")
    application.include_router(candidates.router, prefix="/api")
    application.include_router(companies.router, prefix="/api")
    application.include_router(recruiters.router, prefix="/api")
    application.include_router(jobs.router, prefix="/api")
    application.include_router(applications.router, prefix="/api")
    application.include_router(notifications.router, prefix="/api")
    application.include_router(admin.router, prefix="/api")

    if SITE_ROOT.joinpath("index.html").exists() and settings.app_env != "test":
        application.mount("/", StaticFiles(directory=str(SITE_ROOT), html=True), name="site")
    return application


app = create_app()
