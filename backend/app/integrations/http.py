"""Client HTTP partagé : timeout, retries, journaux sans secrets."""

from __future__ import annotations

import logging
import time
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import httpx

from app.config import get_settings
from app.integrations.errors import IntegrationError, map_http_error
from app.integrations.logging import record_call

logger = logging.getLogger("talendus.integrations.http")

_SENSITIVE = ("authorization", "x-api-key", "api-key", "proxy-authorization", "stripe-signature")
_override: httpx.Client | None = None


@contextmanager
def override_client(client: httpx.Client) -> Iterator[httpx.Client]:
    global _override
    previous = _override
    _override = client
    try:
        yield client
    finally:
        _override = previous


def redact_headers(headers: dict | None) -> dict:
    clean: dict[str, str] = {}
    for key, value in (headers or {}).items():
        if str(key).lower() in _SENSITIVE or "token" in str(key).lower() or "secret" in str(key).lower():
            clean[str(key)] = "[redacted]"
        else:
            clean[str(key)] = str(value)
    return clean


def request(
    method: str,
    url: str,
    *,
    provider: str,
    operation: str,
    headers: dict | None = None,
    json: Any = None,
    params: dict | None = None,
    data: Any = None,
    timeout: float | None = None,
    retries: int | None = None,
) -> httpx.Response:
    settings = get_settings()
    timeout = timeout if timeout is not None else float(settings.integrations_timeout_seconds)
    retries = retries if retries is not None else int(settings.integrations_max_retries)
    safe_params = {k: ("[redacted]" if "key" in k.lower() or "token" in k.lower() else v) for k, v in (params or {}).items()}
    last_exc: Exception | None = None
    started = time.perf_counter()
    attempts = max(1, retries + 1)
    for attempt in range(attempts):
        try:
            client = _override or httpx.Client(timeout=timeout)
            close = _override is None
            try:
                response = client.request(method, url, headers=headers, json=json, params=params, data=data)
            finally:
                if close:
                    client.close()
            duration = int((time.perf_counter() - started) * 1000)
            request_id = response.headers.get("x-request-id") or response.headers.get("request-id")
            if response.status_code in {429, 502, 503} and attempt < attempts - 1:
                logger.warning(
                    "integration retry provider=%s op=%s status=%s attempt=%s headers=%s params=%s",
                    provider,
                    operation,
                    response.status_code,
                    attempt + 1,
                    redact_headers(headers),
                    safe_params,
                )
                time.sleep(0.05 * (2**attempt))
                continue
            success = 200 <= response.status_code < 300
            record_call(
                provider=provider,
                operation=operation,
                success=success,
                status_code=response.status_code,
                duration_ms=duration,
                request_id=request_id,
                error_code=None if success else f"HTTP_{response.status_code}",
            )
            if not success:
                raise map_http_error(response.status_code, provider, operation)
            return response
        except IntegrationError:
            raise
        except httpx.TimeoutException as exc:
            last_exc = exc
            if attempt < attempts - 1:
                time.sleep(0.05 * (2**attempt))
                continue
            duration = int((time.perf_counter() - started) * 1000)
            record_call(provider=provider, operation=operation, success=False, duration_ms=duration, error_code="INTEGRATION_TIMEOUT")
            raise IntegrationError(
                f"{provider} n'a pas répondu à temps.",
                "INTEGRATION_TIMEOUT",
                provider=provider,
            ) from exc
        except httpx.HTTPError as exc:
            last_exc = exc
            if attempt < attempts - 1:
                time.sleep(0.05 * (2**attempt))
                continue
            duration = int((time.perf_counter() - started) * 1000)
            record_call(provider=provider, operation=operation, success=False, duration_ms=duration, error_code="INTEGRATION_UNAVAILABLE")
            raise IntegrationError(
                f"{provider} est injoignable.",
                "INTEGRATION_UNAVAILABLE",
                provider=provider,
            ) from exc
    duration = int((time.perf_counter() - started) * 1000)
    record_call(provider=provider, operation=operation, success=False, duration_ms=duration, error_code="INTEGRATION_INTERNAL")
    raise IntegrationError(
        f"{provider} a échoué ({operation}).",
        "INTEGRATION_INTERNAL",
        provider=provider,
    ) from last_exc
