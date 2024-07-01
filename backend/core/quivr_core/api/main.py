import logging

from fastapi import FastAPI
from quivr_core.api.modules.brain.controller import brain_router
from quivr_core.api.modules.chat.controller import chat_router
from quivr_core.api.modules.knowledge.controller import knowledge_router
from quivr_core.api.modules.prompt.controller import prompt_router
from quivr_core.api.modules.upload.controller import upload_router
from quivr_core.api.modules.user.controller import user_router

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("LiteLLM").setLevel(logging.WARNING)
logging.getLogger("litellm").setLevel(logging.WARNING)

app = FastAPI()


app.include_router(brain_router)
app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(user_router)
app.include_router(prompt_router)
app.include_router(knowledge_router)


@app.get("/")
async def root():
    return {"status": "OK"}


@app.get("/healthz", tags=["Health"])
async def healthz():
    return {"status": "ok"}


if __name__ == "__main__":
    # run main.py to debug backend
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5050, log_level="debug", access_log=False)
