import logging
import os

import litellm
import sentry_sdk
from dotenv import load_dotenv  # type: ignore
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pyinstrument import Profiler
from quivr_api.logger import get_logger
from quivr_api.middlewares.cors import add_cors_middleware
from quivr_api.modules.analytics.controller.analytics_routes import analytics_router
from quivr_api.modules.api_key.controller import api_key_router
from quivr_api.modules.assistant.controller import assistant_router
from quivr_api.modules.brain.controller import brain_router
from quivr_api.modules.chat.controller import chat_router
from quivr_api.modules.knowledge.controller import knowledge_router
from quivr_api.modules.misc.controller import misc_router
from quivr_api.modules.models.controller.model_routes import model_router
from quivr_api.modules.onboarding.controller import onboarding_router
from quivr_api.modules.prompt.controller import prompt_router
from quivr_api.modules.sync.controller import sync_router
from quivr_api.modules.upload.controller import upload_router
from quivr_api.modules.user.controller import user_router
from quivr_api.packages.utils import handle_request_validation_error
from quivr_api.packages.utils.telemetry import maybe_send_telemetry
from quivr_api.routes.crawl_routes import crawl_router
from quivr_api.routes.subscription_routes import subscription_router
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

load_dotenv()

# Set the logging level for all loggers to WARNING
logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("LiteLLM").setLevel(logging.WARNING)
logging.getLogger("litellm").setLevel(logging.WARNING)
get_logger("quivr_core")
litellm.set_verbose = False


logger = get_logger(__name__)


def before_send(event, hint):
    # If this is a transaction event
    if event["type"] == "transaction":
        # And the transaction name contains 'healthz'
        if "healthz" in event["transaction"]:
            # Drop the event by returning None
            return None
    # For other events, return them as is
    return event


sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        sample_rate=0.1,
        enable_tracing=True,
        traces_sample_rate=0.1,
        integrations=[
            StarletteIntegration(transaction_style="url"),
            FastApiIntegration(transaction_style="url"),
        ],
        before_send=before_send,
    )

app = FastAPI()
add_cors_middleware(app)

app.include_router(brain_router)
app.include_router(chat_router)
app.include_router(crawl_router)
app.include_router(assistant_router)
app.include_router(sync_router)
app.include_router(onboarding_router)
app.include_router(misc_router)
app.include_router(analytics_router)
app.include_router(upload_router)
app.include_router(user_router)
app.include_router(api_key_router)
app.include_router(subscription_router)
app.include_router(prompt_router)
app.include_router(knowledge_router)
app.include_router(model_router)

PROFILING = os.getenv("PROFILING", "false").lower() == "true"


if PROFILING:

    @app.middleware("http")
    async def profile_request(request: Request, call_next):
        profiling = request.query_params.get("profile", False)
        if profiling:
            profiler = Profiler()
            profiler.start()
            await call_next(request)
            profiler.stop()
            return HTMLResponse(profiler.output_html())
        else:
            return await call_next(request)


@app.exception_handler(HTTPException)
async def http_exception_handler(_, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


handle_request_validation_error(app)

if os.getenv("TELEMETRY_ENABLED") == "true":
    logger.info("Telemetry enabled, we use telemetry to collect anonymous usage data.")
    logger.info(
        "To disable telemetry, set the TELEMETRY_ENABLED environment variable to false."
    )
    maybe_send_telemetry("booting", {"status": "ok"})
    maybe_send_telemetry("ping", {"ping": "pong"})


if __name__ == "__main__":
    # run main.py to debug backend
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5050, log_level="debug", access_log=False)
