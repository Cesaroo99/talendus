from typing import Any

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


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


async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=error_body(exc.message, exc.code, exc.details),
    )


async def http_error_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    if isinstance(exc, AppError):
        return await app_error_handler(_request, exc)
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


async def unhandled_handler(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=error_body("Une erreur interne s'est produite.", "INTERNAL_ERROR"),
    )
