import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import pypandoc
from logger import get_logger
from middlewares.cors import add_cors_middleware
from routes.api_key_routes import api_key_router
from routes.brain_routes import brain_router
from routes.chat_routes import chat_router
from routes.crawl_routes import crawl_router
from routes.explore_routes import explore_router
from routes.misc_routes import misc_router
from routes.stream_routes import stream_router
from routes.upload_routes import upload_router
from routes.user_routes import user_router

logger = get_logger(__name__)

app = FastAPI()

add_cors_middleware(app)
max_brain_size = os.getenv("MAX_BRAIN_SIZE")
max_brain_size_with_own_key = os.getenv("MAX_BRAIN_SIZE_WITH_KEY", 209715200)


@app.on_event("startup")
async def startup_event():
    pypandoc.download_pandoc()


app.include_router(brain_router)
app.include_router(chat_router)
app.include_router(crawl_router)
app.include_router(explore_router)
app.include_router(misc_router)
app.include_router(upload_router)
app.include_router(user_router)
app.include_router(api_key_router)
app.include_router(stream_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
