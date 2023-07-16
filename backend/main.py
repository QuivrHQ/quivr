import os

import pypandoc
import sentry_sdk
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import HTMLResponse
from fastapi.responses import JSONResponse
from logger import get_logger
from middlewares.cors import add_cors_middleware
from routes.api_key_routes import api_key_router
from routes.brain_routes import brain_router
from routes.chat_routes import chat_router
from routes.crawl_routes import crawl_router
from routes.explore_routes import explore_router
from routes.misc_routes import misc_router
from routes.subscription_routes import subscription_router
from routes.upload_routes import upload_router
from routes.user_routes import user_router

logger = get_logger(__name__)

sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0,
    )

app = FastAPI()

add_cors_middleware(app)


@app.on_event("startup")
async def startup_event():
    if not os.path.exists(pypandoc.get_pandoc_path()):
        pypandoc.download_pandoc()


app.include_router(brain_router)
app.include_router(chat_router)
app.include_router(crawl_router)
app.include_router(explore_router)
app.include_router(misc_router)
app.include_router(upload_router)
app.include_router(user_router)
app.include_router(api_key_router)
app.include_router(subscription_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation() -> HTMLResponse:
    return get_redoc_html(openapi_url="/openapi.json", title="docs")


@app.get("/openapi.json", include_in_schema=False)
async def openapi() -> Dict[str, Any]:
    return get_openapi(title="Qamar", version="0.1.0", routes=app.routes)
