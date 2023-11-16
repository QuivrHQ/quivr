from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from logger import get_logger

logger = get_logger(__name__)


def handle_request_validation_error(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
        logger.error(request, exc_str)
        content = {
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": exc_str,
            "data": None,
        }
        return JSONResponse(
            content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
