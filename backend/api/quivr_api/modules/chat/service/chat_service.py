import random
from typing import List
from uuid import UUID

from fastapi import HTTPException

from quivr_api.logger import get_logger
from quivr_api.modules.brain.entity.brain_entity import Brain
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.chat.dto.chats import ChatItem
from quivr_api.modules.chat.dto.inputs import (
    ChatMessageProperties,
    ChatUpdatableProperties,
    CreateChatHistory,
    CreateChatProperties,
    QuestionAndAnswer,
)
from quivr_api.modules.chat.dto.outputs import GetChatHistoryOutput
from quivr_api.modules.chat.entity.chat import Chat, ChatHistory
from quivr_api.modules.chat.repository.chats import ChatRepository
from quivr_api.modules.chat.service.utils import merge_chat_history_and_notifications
from quivr_api.modules.dependencies import BaseService
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.prompt.entity.prompt import Prompt
from quivr_api.modules.prompt.service.prompt_service import PromptService

logger = get_logger(__name__)

prompt_service = PromptService()
brain_service = BrainService()
notification_service = NotificationService()


class ChatService(BaseService[ChatRepository]):
    repository_cls = ChatRepository

    def __init__(self, repository: ChatRepository):
        self.repository = repository

    async def create_chat(
        self, user_id: UUID, new_chat_data: CreateChatProperties
    ) -> Chat:
        # Chat is created upon the user's first question asked
        logger.info(f"New chat entry in chats table for user {user_id}")

        inserted_chat = await self.repository.create_chat(
            Chat(chat_name=new_chat_data.name, user_id=user_id)
        )
        logger.info(f"Insert response {inserted_chat}")

        return inserted_chat

    def get_follow_up_question(
        self, brain_id: UUID | None = None, question: str | None = None
    ) -> [str]:
        follow_up = [
            "Summarize the conversation",
            "Explain in more detail",
            "Explain like I'm 5",
            "Provide a list",
            "Give examples",
            "Use simpler language",
            "Elaborate on a specific point",
            "Provide pros and cons",
            "Break down into steps",
            "Illustrate with an image or diagram",
        ]
        # Return 3 random follow up questions amongs the list
        random3 = random.sample(follow_up, 3)
        return random3

    async def add_question_and_answer(
        self, chat_id: UUID, question_and_answer: QuestionAndAnswer
    ) -> ChatHistory:
        return await self.repository.add_question_and_answer(
            chat_id, question_and_answer
        )

    async def get_chat_by_id(self, chat_id: UUID) -> Chat:
        chat = await self.repository.get_chat_by_id(chat_id)
        return chat

    async def get_chat_history(self, chat_id: UUID) -> List[GetChatHistoryOutput]:
        history = await self.repository.get_chat_history(chat_id)
        enriched_history: List[GetChatHistoryOutput] = []
        if len(history) == 0:
            return enriched_history
        for message in history:
            brain: Brain | None = (
                await message.awaitable_attrs.brain if message.brain_id else None
            )
            prompt: Prompt | None = None
            if brain:
                prompt = (
                    await brain.awaitable_attrs.prompt if message.prompt_id else None
                )
            enriched_history.append(
                # TODO : WHY bother with having ids here ??
                GetChatHistoryOutput(
                    chat_id=(message.chat_id),
                    message_id=message.message_id,
                    user_message=message.user_message,
                    assistant=message.assistant,
                    message_time=message.message_time,
                    brain_name=brain.name if brain else None,
                    brain_id=brain.brain_id if brain else None,
                    prompt_title=(prompt.title if prompt else None),
                    metadata=message.metadata_,
                    thumbs=message.thumbs,
                )
            )
        return enriched_history

    async def get_chat_history_with_notifications(
        self,
        chat_id: UUID,
    ) -> List[ChatItem]:
        chat_history = await self.get_chat_history(chat_id)
        chat_notifications = []
        return merge_chat_history_and_notifications(chat_history, chat_notifications)

    async def get_user_chats(self, user_id: UUID) -> List[Chat]:
        return list(await self.repository.get_user_chats(user_id))

    def update_chat_history(self, chat_history: CreateChatHistory) -> ChatHistory:
        response: List[ChatHistory] = (
            self.repository.update_chat_history(chat_history)
        ).data
        if len(response) == 0:
            raise HTTPException(
                status_code=500,
                detail="An exception occurred while updating chat history.",
            )
        return ChatHistory(**response[0])  # pyright: ignore reportPrivateUsage=none

    def update_chat(self, chat_id, chat_data: ChatUpdatableProperties) -> Chat:
        if not chat_id:
            logger.error("No chat_id provided")
            return  # pyright: ignore reportPrivateUsage=none

        updates = {}

        if chat_data.chat_name is not None:
            updates["chat_name"] = chat_data.chat_name

        updated_chat = None

        if updates:
            updated_chat = (self.repository.update_chat(chat_id, updates)).data[0]
            logger.info(f"Chat {chat_id} updated")
        else:
            logger.info(f"No updates to apply for chat {chat_id}")
        return updated_chat  # pyright: ignore reportPrivateUsage=none

    def update_message_by_id(
        self,
        message_id: str,
        user_message: str = None,  # pyright: ignore reportPrivateUsage=none
        assistant: str = None,  # pyright: ignore reportPrivateUsage=none
        metadata: dict = None,  # pyright: ignore reportPrivateUsage=none
    ) -> ChatHistory:
        if not message_id:
            logger.error("No message_id provided")
            return  # pyright: ignore reportPrivateUsage=none

        updates = {}

        if user_message is not None:
            updates["user_message"] = user_message

        if assistant is not None:
            updates["assistant"] = assistant

        if metadata is not None:
            updates["metadata"] = metadata

        updated_message = None

        if updates:
            updated_message = (
                self.repository.update_message_by_id(message_id, updates)
            ).data[  # type: ignore
                0
            ]
            logger.info(f"Message {message_id} updated")
        else:
            logger.info(f"No updates to apply for message {message_id}")
        return ChatHistory(**updated_message)  # pyright: ignore reportPrivateUsage=none

    def delete_chat_from_db(self, chat_id):
        try:
            self.repository.delete_chat_history(chat_id)
        except Exception as e:
            print(e)
            pass
        try:
            self.repository.delete_chat(chat_id)
        except Exception as e:
            print(e)
            pass

    def update_chat_message(
        self, chat_id, message_id, chat_message_properties: ChatMessageProperties
    ):
        try:
            return self.repository.update_chat_message(
                chat_id, message_id, chat_message_properties
            ).data
        except Exception as e:
            print(e)
            pass
