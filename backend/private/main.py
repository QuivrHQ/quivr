import os

import sentry_sdk
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from logger import get_logger
from routes.completions_routes import completions_router

logger = get_logger(__name__)

if os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,
    )

app = FastAPI()

app.include_router(completions_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
