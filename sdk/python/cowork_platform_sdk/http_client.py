"""Async HTTP client factory for cowork backend services.

Provides a pre-configured httpx.AsyncClient with:
- Connection pooling
- Default timeouts
- Structured error parsing
- Request ID propagation
"""

from __future__ import annotations

import uuid
from typing import Any

import httpx

from cowork_platform_sdk.errors import CoworkAPIError, InternalError


def create_http_client(
    base_url: str,
    *,
    timeout: float = 30.0,
    max_connections: int = 20,
) -> httpx.AsyncClient:
    """Create a pre-configured httpx.AsyncClient for a cowork backend service.

    Args:
        base_url: The base URL of the service (e.g., "http://localhost:8001").
        timeout: Default request timeout in seconds.
        max_connections: Maximum number of connections in the pool.

    Returns:
        A configured httpx.AsyncClient instance. Caller is responsible for closing it.
    """
    return httpx.AsyncClient(
        base_url=base_url,
        timeout=httpx.Timeout(timeout),
        limits=httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_connections,
        ),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        event_hooks={
            "request": [_inject_request_id],
        },
    )


async def _inject_request_id(request: httpx.Request) -> None:
    """Add a unique request ID header if not already present."""
    if "X-Request-ID" not in request.headers:
        request.headers["X-Request-ID"] = str(uuid.uuid4())


def parse_error_response(response: httpx.Response) -> CoworkAPIError:
    """Parse an HTTP error response into a typed CoworkAPIError.

    Args:
        response: The httpx response with a 4xx or 5xx status code.

    Returns:
        A CoworkAPIError (or subclass) matching the error code.
    """
    try:
        data: dict[str, Any] = response.json()
        return CoworkAPIError.from_dict(data)
    except Exception:
        return InternalError(
            message=f"HTTP {response.status_code}: {response.text[:200]}",
            details={"status_code": response.status_code},
        )


async def raise_for_status(response: httpx.Response) -> None:
    """Raise a CoworkAPIError if the response indicates an error.

    Use as: `await raise_for_status(response)` after each HTTP call.
    """
    if response.status_code >= 400:
        raise parse_error_response(response)
