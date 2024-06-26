from typing import Sequence
from uuid import UUID

from quivr_api.models.settings import get_supabase_client
from quivr_api.modules.chat.dto.inputs import ChatMessageProperties, QuestionAndAnswer
from quivr_api.modules.chat.entity.chat import Chat, ChatHistory
from quivr_api.modules.dependencies import BaseRepository
from sqlalchemy import exc
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession


class ChatRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        # TODO: for now use it instead of session
        self.db = get_supabase_client()

    async def get_user_chats(self, user_id: UUID) -> Sequence[Chat]:
        query = select(Chat).where(Chat.user_id == user_id)
        response = await self.session.exec(query)
        return response.all()

    async def create_chat(self, new_chat: Chat) -> Chat:
        try:
            self.session.add(new_chat)
            await self.session.commit()
        except exc.IntegrityError:
            await self.session.rollback()
            # TODO(@aminediro): Custom exceptions
            raise Exception()

        await self.session.refresh(new_chat)
        return new_chat

    async def get_chat_by_id(self, chat_id: UUID):
        query = select(Chat).where(Chat.chat_id == chat_id)
        response = await self.session.exec(query)
        return response.one()

    async def get_chat_history(self, chat_id: UUID) -> Sequence[ChatHistory]:
        query = (
            select(ChatHistory).where(ChatHistory.chat_id == chat_id)
            # TODO: type hints of sqlmodel arent stable for order_by
            .order_by(ChatHistory.message_time)  # type: ignore
        )
        response = await self.session.exec(query)
        return response.all()

    async def add_question_and_answer(
        self, chat_id: UUID, question_and_answer: QuestionAndAnswer
    ) -> ChatHistory:
        chat = ChatHistory(
            chat_id=chat_id,
            user_message=question_and_answer.question,
            assistant=question_and_answer.answer,
        )
        try:
            self.session.add(chat)
            await self.session.commit()
        except exc.IntegrityError:
            await self.session.rollback()
            # TODO(@aminediro) : for now, build an exception system
            raise Exception("can't create chat_history ")
        await self.session.refresh(chat)
        return chat

    def update_chat_history(self, chat_history):
        response = (
            self.db.table("chat_history")
            .insert(
                {
                    "chat_id": str(chat_history.chat_id),
                    "user_message": chat_history.user_message,
                    "assistant": chat_history.assistant,
                    "prompt_id": (
                        str(chat_history.prompt_id) if chat_history.prompt_id else None
                    ),
                    "brain_id": (
                        str(chat_history.brain_id) if chat_history.brain_id else None
                    ),
                    "metadata": chat_history.metadata if chat_history.metadata else {},
                }
            )
            .execute()
        )
        return response

    def update_chat(self, chat_id, updates):
        response = (
            self.db.table("chats").update(updates).match({"chat_id": chat_id}).execute()
        )

        return response

    def update_message_by_id(self, message_id, updates):
        response = (
            self.db.table("chat_history")
            .update(updates)
            .match({"message_id": message_id})
            .execute()
        )

        return response

    def delete_chat(self, chat_id):
        self.db.table("chats").delete().match({"chat_id": chat_id}).execute()

    def delete_chat_history(self, chat_id):
        self.db.table("chat_history").delete().match({"chat_id": chat_id}).execute()

    def update_chat_message(
        self, chat_id, message_id, chat_message_properties: ChatMessageProperties
    ):
        response = (
            self.db.table("chat_history")
            .update(chat_message_properties)
            .match({"message_id": message_id, "chat_id": chat_id})
            .execute()
        )

        return response
