from dotenv import load_dotenv
from fastapi import FastAPI

from quivr_core.api.modules.brain.controller import brain_router
from quivr_core.api.modules.chat.controller import chat_router
from quivr_core.api.modules.knowledge.controller import knowledge_router
from quivr_core.api.modules.prompt.controller import prompt_router
from quivr_core.api.modules.upload.controller import upload_router
from quivr_core.api.modules.user.controller import user_router

load_dotenv()

app = FastAPI()


app.include_router(brain_router)
app.include_router(chat_router)

app.include_router(upload_router)
app.include_router(user_router)
app.include_router(prompt_router)
app.include_router(knowledge_router)
