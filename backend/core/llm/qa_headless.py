from uuid import UUID

from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.llms.base import BaseLLM
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from models.databases.supabase.chats import CreateChatHistory
from repository.chat.format_chat_history import format_chat_history
from repository.chat.get_chat_history import get_chat_history
from repository.chat.update_chat_history import update_chat_history
from repository.chat.format_chat_history import format_history_to_openai_mesages
from logger import get_logger
from models.chats import ChatQuestion
from repository.chat.get_chat_history import GetChatHistoryOutput


from pydantic import BaseModel

from typing import AsyncIterable, List

logger = get_logger(__name__)
SYSTEM_MESSAGE = "Your name is Quivr. You're a helpful assistant.  If you don't know the answer, just say that you don't know, don't try to make up an answer."


class HeadlessQA(BaseModel):
    model: str = None  # type: ignore
    temperature: float = 0.0
    max_tokens: int = 256
    user_openai_api_key: str = None  # type: ignore
    openai_api_key: str = None  # type: ignore
    streaming: bool = False
    chat_id: str = None  # type: ignore
    callbacks: List[AsyncIteratorCallbackHandler] = None  # type: ignore

    def _determine_api_key(self, openai_api_key, user_openai_api_key):
        """If user provided an API key, use it."""
        if user_openai_api_key is not None:
            return user_openai_api_key
        else:
            return openai_api_key

    def _determine_streaming(self, model: str, streaming: bool) -> bool:
        """If the model name allows for streaming and streaming is declared, set streaming to True."""
        return streaming

    def _determine_callback_array(
        self, streaming
    ) -> List[AsyncIteratorCallbackHandler]:  # pyright: ignore reportPrivateUsage=none
        """If streaming is set, set the AsyncIteratorCallbackHandler as the only callback."""
        if streaming:
            return [
                AsyncIteratorCallbackHandler()  # pyright: ignore reportPrivateUsage=none
            ]

    def __init__(self, **data):
        super().__init__(**data)

        self.openai_api_key = self._determine_api_key(
            self.openai_api_key, self.user_openai_api_key
        )
        self.streaming = self._determine_streaming(
            self.model, self.streaming
        )  # pyright: ignore reportPrivateUsage=none
        self.callbacks = self._determine_callback_array(
            self.streaming
        )  # pyright: ignore reportPrivateUsage=none

    def _create_llm(
        self, model, temperature=0, streaming=False, callbacks=None
    ) -> BaseLLM:
        """
        Determine the language model to be used.
        :param model: Language model name to be used.
        :param streaming: Whether to enable streaming of the model
        :param callbacks: Callbacks to be used for streaming
        :return: Language model instance
        """
        return ChatOpenAI(
            temperature=temperature,
            model=model,
            streaming=streaming,
            verbose=True,
            callbacks=callbacks,
            openai_api_key=self.openai_api_key,
        )  # pyright: ignore reportPrivateUsage=none

    def _create_prompt_template(self):
        messages = [
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
        CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)
        return CHAT_PROMPT

    def generate_answer(
        self, chat_id: UUID, question: ChatQuestion
    ) -> GetChatHistoryOutput:
        transformed_history = format_chat_history(get_chat_history(self.chat_id))
        messages = format_history_to_openai_mesages(transformed_history, SYSTEM_MESSAGE, question.question)
        answering_llm = self._create_llm(
            model=self.model, streaming=False, callbacks=self.callbacks
        )
        model_prediction = answering_llm.predict_messages(messages)  # pyright: ignore reportPrivateUsage=none
        answer = model_prediction.content

        new_chat = update_chat_history(
            CreateChatHistory(
                **{
                    "chat_id": chat_id,
                    "user_message": question.question,
                    "assistant": answer,
                    "brain_id": None,
                    "prompt_id": None,
                }
            )
        )

        return GetChatHistoryOutput(
            **{
                "chat_id": chat_id,
                "user_message": question.question,
                "assistant": answer,
                "message_time": new_chat.message_time,
                "prompt_title": None,
                "brain_name": None,
                "message_id": new_chat.message_id,
            }
        )

    async def generate_stream(
        self, chat_id: UUID, question: ChatQuestion
    ) -> AsyncIterable:
        # TODO
        return

    class Config:
        arbitrary_types_allowed = True
