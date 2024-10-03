import os
import time
import uuid

import structlog
from fastapi import Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import (
    bind_contextvars,
    clear_contextvars,
)

logger = structlog.stdlib.get_logger("quivr_api.access")


git_sha = os.getenv("PORTER_IMAGE_TAG", None)


def clean_dict(d):
    """Remove None values from a dictionary."""
    return {k: v for k, v in d.items() if v is not None}


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        clear_contextvars()
        # Generate a unique request ID
        request_id = str(uuid.uuid4())

        client_addr = (
            f"{request.client.host}:{request.client.port}" if request.client else None
        )
        url = request.url.path
        http_version = request.scope["http_version"]

        bind_contextvars(
            **clean_dict(
                {
                    "git_head": git_sha,
                    "request_id": request_id,
                    "method": request.method,
                    "query_params": dict(request.query_params),
                    "client_addr": client_addr,
                    "request_user_agent": request.headers.get("user-agent"),
                    "request_content_type": request.headers.get("content-type"),
                    "url": url,
                    "http_version": http_version,
                }
            )
        )

        # Start time
        start_time = time.perf_counter()
        response = Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            # Process the request
            response: Response = await call_next(request)
            process_time = time.perf_counter() - start_time
            bind_contextvars(
                **clean_dict(
                    {
                        "response_content_type": response.headers.get("content-type"),
                        "response_status": response.status_code,
                        "response_headers": dict(response.headers),
                        "timing_request_total_ms": round(process_time * 1e3, 3),
                    }
                )
            )

            logger.info(
                f"""{client_addr} - "{request.method} {url} HTTP/{http_version}" {response.status_code}""",
            )
        except Exception:
            process_time = time.perf_counter() - start_time
            bind_contextvars(
                **clean_dict(
                    {
                        "response_status": response.status_code,
                        "timing_request_total_ms": round(process_time * 1000, 3),
                    }
                )
            )
            structlog.stdlib.get_logger("quivr_api.error").exception(
                "Request failed with exception"
            )
            raise

        finally:
            clear_contextvars()

        # Add X-Request-ID to response headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)

        return response
