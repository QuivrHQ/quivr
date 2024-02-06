import asyncio
import json
from typing import AsyncIterable, Awaitable, List, Optional
from uuid import UUID

from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.chains import LLMChain
from langchain.chat_models.base import BaseChatModel
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_community.chat_models import ChatLiteLLM
from llm.utils.format_chat_history import (
    format_chat_history,
    format_history_to_openai_mesages,
)
from llm.utils.get_prompt_to_use import get_prompt_to_use
from llm.utils.get_prompt_to_use_id import get_prompt_to_use_id
from logger import get_logger
from models import BrainSettings  # Importing settings related to the 'brain'
from modules.brain.qa_interface import QAInterface
from modules.chat.dto.chats import ChatQuestion
from modules.chat.dto.inputs import CreateChatHistory
from modules.chat.dto.outputs import GetChatHistoryOutput
from modules.chat.service.chat_service import ChatService
from modules.prompt.entity.prompt import Prompt
from pydantic import BaseModel

logger = get_logger(__name__)
SYSTEM_MESSAGE = "Your name is Quivr. You're a helpful assistant. If you don't know the answer, just say that you don't know, don't try to make up an answer.When answering use markdown or any other techniques to display the content in a nice and aerated way."
chat_service = ChatService()


class HeadlessQA(BaseModel, QAInterface):
    brain_settings = BrainSettings()
    model: str
    temperature: float = 0.0
    max_tokens: int = 2000
    streaming: bool = False
    chat_id: str
    callbacks: Optional[List[AsyncIteratorCallbackHandler]] = None
    prompt_id: Optional[UUID] = None

    def _determine_streaming(self, streaming: bool) -> bool:
        """If the model name allows for streaming and streaming is declared, set streaming to True."""
        return streaming

    def _determine_callback_array(
        self, streaming
    ) -> List[AsyncIteratorCallbackHandler]:
        """If streaming is set, set the AsyncIteratorCallbackHandler as the only callback."""
        if streaming:
            return [AsyncIteratorCallbackHandler()]
        else:
            return []

    def __init__(self, **data):
        super().__init__(**data)
        self.streaming = self._determine_streaming(self.streaming)
        self.callbacks = self._determine_callback_array(self.streaming)

    @property
    def prompt_to_use(self) -> Optional[Prompt]:
        return get_prompt_to_use(None, self.prompt_id)

    @property
    def prompt_to_use_id(self) -> Optional[UUID]:
        return get_prompt_to_use_id(None, self.prompt_id)

    def _create_llm(
        self,
        model,
        temperature=0,
        streaming=False,
        callbacks=None,
    ) -> BaseChatModel:
        """
        Determine the language model to be used.
        :param model: Language model name to be used.
        :param streaming: Whether to enable streaming of the model
        :param callbacks: Callbacks to be used for streaming
        :return: Language model instance
        """
        api_base = None
        if self.brain_settings.ollama_api_base_url and model.startswith("ollama"):
            api_base = self.brain_settings.ollama_api_base_url

        return ChatLiteLLM(
            temperature=temperature,
            model=model,
            streaming=streaming,
            verbose=True,
            callbacks=callbacks,
            max_tokens=self.max_tokens,
            api_base=api_base,
        )

    def _create_prompt_template(self):
        messages = [
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
        CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)
        return CHAT_PROMPT

    def generate_answer(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> GetChatHistoryOutput:
        # Move format_chat_history to chat service ?
        transformed_history = format_chat_history(
            chat_service.get_chat_history(self.chat_id)
        )
        prompt_content = (
            self.prompt_to_use.content if self.prompt_to_use else SYSTEM_MESSAGE
        )

        messages = format_history_to_openai_mesages(
            transformed_history, prompt_content, question.question
        )
        answering_llm = self._create_llm(
            model=self.model,
            streaming=False,
            callbacks=self.callbacks,
        )
        model_prediction = answering_llm.predict_messages(messages)
        answer = model_prediction.content
        if save_answer:
            new_chat = chat_service.update_chat_history(
                CreateChatHistory(
                    **{
                        "chat_id": chat_id,
                        "user_message": question.question,
                        "assistant": answer,
                        "brain_id": None,
                        "prompt_id": self.prompt_to_use_id,
                    }
                )
            )

            return GetChatHistoryOutput(
                **{
                    "chat_id": chat_id,
                    "user_message": question.question,
                    "assistant": answer,
                    "message_time": new_chat.message_time,
                    "prompt_title": (
                        self.prompt_to_use.title if self.prompt_to_use else None
                    ),
                    "brain_name": None,
                    "message_id": new_chat.message_id,
                }
            )
        else:
            return GetChatHistoryOutput(
                **{
                    "chat_id": chat_id,
                    "user_message": question.question,
                    "assistant": answer,
                    "message_time": None,
                    "prompt_title": (
                        self.prompt_to_use.title if self.prompt_to_use else None
                    ),
                    "brain_name": None,
                    "message_id": None,
                }
            )

    async def generate_stream(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> AsyncIterable:
        callback = AsyncIteratorCallbackHandler()
        self.callbacks = [callback]

        transformed_history = format_chat_history(
            chat_service.get_chat_history(self.chat_id)
        )
        prompt_content = (
            self.prompt_to_use.content if self.prompt_to_use else SYSTEM_MESSAGE
        )

        messages = format_history_to_openai_mesages(
            transformed_history, prompt_content, question.question
        )
        answering_llm = self._create_llm(
            model=self.model,
            streaming=True,
            callbacks=self.callbacks,
        )

        CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)
        headlessChain = LLMChain(llm=answering_llm, prompt=CHAT_PROMPT)

        response_tokens = []

        async def wrap_done(fn: Awaitable, event: asyncio.Event):
            try:
                await fn
            except Exception as e:
                logger.error(f"Caught exception: {e}")
            finally:
                event.set()

        run = asyncio.create_task(
            wrap_done(
                headlessChain.acall({}),
                callback.done,
            ),
        )

        if save_answer:
            streamed_chat_history = chat_service.update_chat_history(
                CreateChatHistory(
                    **{
                        "chat_id": chat_id,
                        "user_message": question.question,
                        "assistant": "",
                        "brain_id": None,
                        "prompt_id": self.prompt_to_use_id,
                    }
                )
            )

            streamed_chat_history = GetChatHistoryOutput(
                **{
                    "chat_id": str(chat_id),
                    "message_id": streamed_chat_history.message_id,
                    "message_time": streamed_chat_history.message_time,
                    "user_message": question.question,
                    "assistant": "",
                    "prompt_title": (
                        self.prompt_to_use.title if self.prompt_to_use else None
                    ),
                    "brain_name": None,
                }
            )
        else:
            streamed_chat_history = GetChatHistoryOutput(
                **{
                    "chat_id": str(chat_id),
                    "message_id": None,
                    "message_time": None,
                    "user_message": question.question,
                    "assistant": "",
                    "prompt_title": (
                        self.prompt_to_use.title if self.prompt_to_use else None
                    ),
                    "brain_name": None,
                }
            )

        async for token in callback.aiter():
            response_tokens.append(token)
            streamed_chat_history.assistant = token
            yield f"data: {json.dumps(streamed_chat_history.dict())}"

        await run
        assistant = "".join(response_tokens)

        if save_answer:
            chat_service.update_message_by_id(
                message_id=str(streamed_chat_history.message_id),
                user_message=question.question,
                assistant=assistant,
            )

    class Config:
        arbitrary_types_allowed = True
