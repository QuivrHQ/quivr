import os

import pypandoc
from auth.auth_bearer import JWTBearer
from fastapi import FastAPI
from logger import get_logger
from middlewares.cors import add_cors_middleware
from models.chats import ChatMessage
from models.users import User
from routes.chat_routes import chat_router
from routes.crawl_routes import crawl_router
from routes.explore_routes import explore_router
from routes.misc_routes import misc_router
from routes.upload_routes import upload_router
from routes.user_routes import user_router
from utils.vectors import (CommonsDep, create_user, similarity_search,
                           update_user_request_count)

logger = get_logger(__name__)

app = FastAPI()


add_cors_middleware(app)
max_brain_size = os.getenv("MAX_BRAIN_SIZE")
max_brain_size_with_own_key = os.getenv("MAX_BRAIN_SIZE_WITH_KEY",209715200)


@app.on_event("startup")
async def startup_event():
    pypandoc.download_pandoc()


app.include_router(chat_router)
app.include_router(crawl_router)
app.include_router(explore_router)
app.include_router(misc_router)
app.include_router(upload_router)
app.include_router(user_router)
