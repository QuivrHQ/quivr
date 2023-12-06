from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from llm.knowledge_brain_qa import KnowledgeBrainQA
from logger import get_logger
from modules.brain.service.brain_service import BrainService
from modules.chat.dto.chats import ChatQuestion
from modules.chat.service.chat_service import ChatService

brain_service = BrainService()
chat_service = ChatService()

logger = get_logger(__name__)


class CompositeBrainQA(
    KnowledgeBrainQA,
):
    user_id: UUID

    def __init__(
        self,
        model: str,
        brain_id: str,
        chat_id: str,
        streaming: bool = False,
        prompt_id: Optional[UUID] = None,
        **kwargs,
    ):
        user_id = kwargs.get("user_id")
        if not user_id:
            raise HTTPException(status_code=400, detail="Cannot find user id")

        super().__init__(
            model=model,
            brain_id=brain_id,
            chat_id=chat_id,
            streaming=streaming,
            prompt_id=prompt_id,
            **kwargs,
        )
        self.user_id = user_id

    async def generate_stream(self, chat_id: UUID, question: ChatQuestion):
        pass

    async def generate_answer(self, chat_id: UUID, question: ChatQuestion):
        pass
