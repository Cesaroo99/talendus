from pathlib import Path
from typing import Any

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse


class AppError(HTTPException):
    def __init__(self, status_code: int, message: str, code: str, details: Any = None):
        super().__init__(status_code=status_code, detail=message)
        self.message = message
        self.code = code
        self.details = details or []


def error_body(message: str, code: str, details: Any = None) -> dict:
    return {
        "success": False,
        "message": message,
        "code": code,
        "details": details or [],
    }


def ok(data: Any = None, message: str | None = None, meta: dict | None = None) -> dict:
    payload: dict[str, Any] = {"success": True, "data": data}
    if message:
        payload["message"] = message
    if meta:
        payload["meta"] = meta
    return payload


SITE_ROOT = Path(__file__).resolve().parents[2]
ERROR_PAGE = SITE_ROOT / "500.html"
NOT_FOUND_PAGE = SITE_ROOT / "404.html"


def wants_html(request: Request) -> bool:
    path = request.url.path
    if path.startswith("/api/") or path.endswith((".xml", ".txt", ".json")):
        return False
    accept = request.headers.get("accept", "")
    return "text/html" in accept or accept == "" or "*/*" in accept


def html_error(status_code: int, fallback_path: Path | None = None) -> HTMLResponse | FileResponse | JSONResponse:
    page = fallback_path if fallback_path and fallback_path.exists() else ERROR_PAGE
    if page.exists():
        return FileResponse(page, status_code=status_code, media_type="text/html; charset=utf-8")
    return HTMLResponse(
        "<!doctype html><html><body><h1>Talendus</h1><p>Service momentanément indisponible.</p></body></html>",
        status_code=status_code,
    )


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse | FileResponse | HTMLResponse:
    if wants_html(request) and exc.status_code in {404, 500, 502, 503}:
        page = NOT_FOUND_PAGE if exc.status_code == 404 else ERROR_PAGE
        return html_error(exc.status_code, page)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_body(exc.message, exc.code, exc.details),
    )


async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse | FileResponse | HTMLResponse:
    if isinstance(exc, AppError):
        return await app_error_handler(request, exc)
    if wants_html(request) and exc.status_code in {404, 500, 502, 503}:
        page = NOT_FOUND_PAGE if exc.status_code == 404 else ERROR_PAGE
        return html_error(exc.status_code, page)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_body(str(exc.detail), "HTTP_ERROR"),
    )


async def validation_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    details = []
    for err in exc.errors():
        loc = ".".join(str(p) for p in err.get("loc", []) if p != "body")
        details.append({"field": loc, "message": err.get("msg")})
    return JSONResponse(
        status_code=422,
        content=error_body("Les données envoyées sont invalides.", "VALIDATION_ERROR", details),
    )


async def unhandled_handler(request: Request, _exc: Exception) -> JSONResponse | FileResponse | HTMLResponse:
    if wants_html(request):
        return html_error(500, ERROR_PAGE)
    return JSONResponse(
        status_code=500,
        content=error_body("Une erreur interne s'est produite.", "INTERNAL_ERROR"),
    )
