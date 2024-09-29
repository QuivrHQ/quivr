import uuid

from fastapi import Request, Response
from starlette.datastructures import Headers
from starlette.middleware.base import BaseHTTPMiddleware

from quivr_api.logger import get_logger

logger = get_logger("quivr-api")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate a unique request ID
        request_id = str(uuid.uuid4())

        user_id = request.state.user.id if hasattr(request.state, "user") else None
        headers = Headers({**request.headers, "X-Request-ID": request_id})
        request._headers = headers

        # Log request details
        request_info = {
            "request_id": request_id,
            "user_id": user_id,
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
            "query_params": dict(request.query_params),
            "client": f"{request.client.host}:{request.client.port}"
            if request.client
            else None,
        }

        logger.info("Request received", extra=request_info)

        # Process the request
        response: Response = await call_next(request)

        # Log response details
        response_info = {
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "user_id": user_id,
            "query_params": dict(request.query_params),
            "client": f"{request.client.host}:{request.client.port}"
            if request.client
            else None,
            "status_code": response.status_code,
            "headers": dict(response.headers),
        }

        logger.info("Response sent", extra=response_info)

        response.headers["X-Request-ID"] = request_id

        return response
