import random
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from logger import get_logger
from modules.brain.service.brain_service import BrainService
from modules.chat.dto.chats import ChatItem
from modules.chat.dto.inputs import (
    ChatMessageProperties,
    ChatUpdatableProperties,
    CreateChatHistory,
    CreateChatProperties,
    QuestionAndAnswer,
)
from modules.chat.dto.outputs import GetChatHistoryOutput
from modules.chat.entity.chat import Chat, ChatHistory
from modules.chat.repository.chats import Chats
from modules.chat.repository.chats_interface import ChatsInterface
from modules.chat.service.utils import merge_chat_history_and_notifications
from modules.notification.service.notification_service import NotificationService
from modules.prompt.service.prompt_service import PromptService

logger = get_logger(__name__)

prompt_service = PromptService()
brain_service = BrainService()
notification_service = NotificationService()


class ChatService:
    repository: ChatsInterface

    def __init__(self):
        self.repository = Chats()

    def create_chat(self, user_id: UUID, chat_data: CreateChatProperties) -> Chat:
        # Chat is created upon the user's first question asked
        logger.info(f"New chat entry in chats table for user {user_id}")

        # Insert a new row into the chats table
        new_chat = {
            "user_id": str(user_id),
            "chat_name": chat_data.name,
        }
        insert_response = self.repository.create_chat(new_chat)
        logger.info(f"Insert response {insert_response.data}")

        return insert_response.data[0]

    def get_follow_up_question(
        self, brain_id: UUID = None, question: str = None
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

    def add_question_and_answer(
        self, chat_id: UUID, question_and_answer: QuestionAndAnswer
    ) -> Optional[Chat]:
        return self.repository.add_question_and_answer(chat_id, question_and_answer)

    def get_chat_by_id(self, chat_id: str) -> Chat:
        response = self.repository.get_chat_by_id(chat_id)
        return Chat(response.data[0])

    def get_chat_history(self, chat_id: str) -> List[GetChatHistoryOutput]:
        history: List[dict] = self.repository.get_chat_history(chat_id).data
        if history is None:
            return []
        else:
            enriched_history: List[GetChatHistoryOutput] = []
            for message in history:
                message = ChatHistory(message)
                brain = None
                if message.brain_id:
                    brain = brain_service.get_brain_by_id(message.brain_id)

                prompt = None
                if message.prompt_id:
                    prompt = prompt_service.get_prompt_by_id(message.prompt_id)

                enriched_history.append(
                    GetChatHistoryOutput(
                        chat_id=(UUID(message.chat_id)),
                        message_id=(UUID(message.message_id)),
                        user_message=message.user_message,
                        assistant=message.assistant,
                        message_time=message.message_time,
                        brain_name=brain.name if brain else None,
                        brain_id=str(brain.id) if brain else None,
                        prompt_title=prompt.title if prompt else None,
                        metadata=message.metadata,
                        thumbs=message.thumbs,
                    )
                )
            return enriched_history

    def get_chat_history_with_notifications(
        self,
        chat_id: UUID,
    ) -> List[ChatItem]:
        chat_history = self.get_chat_history(str(chat_id))
        chat_notifications = notification_service.get_chat_notifications(chat_id)
        return merge_chat_history_and_notifications(chat_history, chat_notifications)

    def get_user_chats(self, user_id: str) -> List[Chat]:
        response = self.repository.get_user_chats(user_id)
        chats = [Chat(chat_dict) for chat_dict in response.data]
        return chats

    def update_chat_history(self, chat_history: CreateChatHistory) -> ChatHistory:
        response: List[ChatHistory] = (
            self.repository.update_chat_history(chat_history)
        ).data
        if len(response) == 0:
            raise HTTPException(
                status_code=500,
                detail="An exception occurred while updating chat history.",
            )
        return ChatHistory(response[0])  # pyright: ignore reportPrivateUsage=none

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
            updated_message = (self.repository.update_message_by_id(message_id, updates)).data[  # type: ignore
                0
            ]
            logger.info(f"Message {message_id} updated")
        else:
            logger.info(f"No updates to apply for message {message_id}")
        return ChatHistory(updated_message)  # pyright: ignore reportPrivateUsage=none

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
