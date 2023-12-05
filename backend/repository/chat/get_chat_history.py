from typing import List, Optional
from uuid import UUID

from models import ChatHistory, get_supabase_db
from pydantic import BaseModel

from repository.brain import get_brain_by_id
from repository.prompt import get_prompt_by_id


class GetChatHistoryOutput(BaseModel):
    chat_id: UUID
    message_id: UUID
    user_message: str
    assistant: str
    message_time: str
    prompt_title: Optional[str] | None
    brain_name: Optional[str] | None

    def dict(self, *args, **kwargs):
        chat_history = super().dict(*args, **kwargs)
        chat_history["chat_id"] = str(chat_history.get("chat_id"))
        chat_history["message_id"] = str(chat_history.get("message_id"))

        return chat_history


def get_chat_history(chat_id: str) -> List[GetChatHistoryOutput]:
    supabase_db = get_supabase_db()
    history: List[dict] = supabase_db.get_chat_history(chat_id).data
    if history is None:
        return []
    else:
        enriched_history: List[GetChatHistoryOutput] = []
        for message in history:
            message = ChatHistory(message)
            brain = None
            if message.brain_id:
                brain = get_brain_by_id(message.brain_id)

            prompt = None
            if message.prompt_id:
                prompt = get_prompt_by_id(message.prompt_id)

            enriched_history.append(
                GetChatHistoryOutput(
                    chat_id=(UUID(message.chat_id)),
                    message_id=(UUID(message.message_id)),
                    user_message=message.user_message,
                    assistant=message.assistant,
                    message_time=message.message_time,
                    brain_name=brain.name if brain else None,
                    prompt_title=prompt.title if prompt else None,
                )
            )
        return enriched_history
