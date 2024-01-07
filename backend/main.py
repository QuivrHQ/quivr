import os

if __name__ == "__main__":
    # import needed here when running main.py to debug backend
    # you will need to run pip install python-dotenv
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
import sentry_sdk
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from logger import get_logger
from middlewares.cors import add_cors_middleware
from modules.api_key.controller import api_key_router
from modules.brain.controller import brain_router
from modules.chat.controller import chat_router
from modules.contact_support.controller import contact_router
from modules.knowledge.controller import knowledge_router
from modules.misc.controller import misc_router
from modules.notification.controller import notification_router
from modules.onboarding.controller import onboarding_router
from modules.prompt.controller import prompt_router
from modules.upload.controller import upload_router
from modules.user.controller import user_router
from packages.utils import handle_request_validation_error
from routes.crawl_routes import crawl_router
from routes.subscription_routes import subscription_router
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

logger = get_logger(__name__)

if os.getenv("DEV_MODE") == "true":
    import debugpy

    logger.debug("👨‍💻 Running in dev mode")
    debugpy.listen(("0.0.0.0", 5678))


sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        sample_rate=0.1,
        enable_tracing=True,
        integrations=[
            StarletteIntegration(transaction_style="endpoint"),
            FastApiIntegration(transaction_style="endpoint"),
        ],
    )

app = FastAPI()

add_cors_middleware(app)

app.include_router(brain_router)
app.include_router(chat_router)
app.include_router(crawl_router)
app.include_router(onboarding_router)
app.include_router(misc_router)

app.include_router(upload_router)
app.include_router(user_router)
app.include_router(api_key_router)
app.include_router(subscription_router)
app.include_router(prompt_router)
app.include_router(notification_router)
app.include_router(knowledge_router)
app.include_router(contact_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


handle_request_validation_error(app)

if __name__ == "__main__":
    # run main.py to debug backend
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5050)
