import asyncio
import json
from typing import AsyncIterable, Awaitable, List, Optional
from uuid import UUID

from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatLiteLLM
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms.base import BaseLLM
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from llm.utils.get_prompt_to_use import get_prompt_to_use
from llm.utils.get_prompt_to_use_id import get_prompt_to_use_id
from logger import get_logger
from models import BrainSettings  # Importing settings related to the 'brain'
from models.chats import ChatQuestion
from models.databases.supabase.chats import CreateChatHistory
from pydantic import BaseModel
from repository.brain import get_brain_by_id
from repository.chat import (
    GetChatHistoryOutput,
    format_chat_history,
    get_chat_history,
    update_chat_history,
    update_message_by_id,
)
from supabase.client import Client, create_client
from vectorstore.supabase import CustomSupabaseVectorStore

from .prompts.CONDENSE_PROMPT import CONDENSE_QUESTION_PROMPT

logger = get_logger(__name__)
QUIVR_DEFAULT_PROMPT = "Your name is Quivr. You're a helpful assistant.  If you don't know the answer, just say that you don't know, don't try to make up an answer."


class QABaseBrainPicking(BaseModel):
    """
    Main class for the Brain Picking functionality.
    It allows to initialize a Chat model, generate questions and retrieve answers using ConversationalRetrievalChain.
    It has two main methods: `generate_question` and `generate_stream`.
    One is for generating questions in a single request, the other is for generating questions in a streaming fashion.
    Both are the same, except that the streaming version streams the last message as a stream.
    Each have the same prompt template, which is defined in the `prompt_template` property.
    """

    class Config:
        """Configuration of the Pydantic Object"""

        # Allowing arbitrary types for class validation
        arbitrary_types_allowed = True

    # Instantiate settings
    brain_settings = BrainSettings()  # type: ignore other parameters are optional

    # Default class attributes
    model: str = None  # pyright: ignore reportPrivateUsage=none
    temperature: float = 0.1
    chat_id: str = None  # pyright: ignore reportPrivateUsage=none
    brain_id: str = None  # pyright: ignore reportPrivateUsage=none
    max_tokens: int = 256
    user_openai_api_key: str = None  # pyright: ignore reportPrivateUsage=none
    streaming: bool = False

    openai_api_key: str = None  # pyright: ignore reportPrivateUsage=none
    callbacks: List[
        AsyncIteratorCallbackHandler
    ] = None  # pyright: ignore reportPrivateUsage=none

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

    @property
    def embeddings(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(
            openai_api_key=self.openai_api_key
        )  # pyright: ignore reportPrivateUsage=none

    supabase_client: Optional[Client] = None
    vector_store: Optional[CustomSupabaseVectorStore] = None
    qa: Optional[ConversationalRetrievalChain] = None
    prompt_id: Optional[UUID]

    def __init__(
        self,
        model: str,
        brain_id: str,
        chat_id: str,
        streaming: bool = False,
        prompt_id: Optional[UUID] = None,
        **kwargs,
    ):
        super().__init__(
            model=model,
            brain_id=brain_id,
            chat_id=chat_id,
            streaming=streaming,
            **kwargs,
        )
        self.supabase_client = self._create_supabase_client()
        self.vector_store = self._create_vector_store()
        self.prompt_id = prompt_id

    @property
    def prompt_to_use(self):
        return get_prompt_to_use(UUID(self.brain_id), self.prompt_id)

    @property
    def prompt_to_use_id(self) -> Optional[UUID]:
        return get_prompt_to_use_id(UUID(self.brain_id), self.prompt_id)

    def _create_supabase_client(self) -> Client:
        return create_client(
            self.brain_settings.supabase_url, self.brain_settings.supabase_service_key
        )

    def _create_vector_store(self) -> CustomSupabaseVectorStore:
        return CustomSupabaseVectorStore(
            self.supabase_client,  # type: ignore
            self.embeddings,  # type: ignore
            table_name="vectors",
            brain_id=self.brain_id,
        )

    def _create_llm(
        self, model, temperature=0, streaming=False, callbacks=None, max_tokens=256
    ) -> BaseLLM:
        """
        Determine the language model to be used.
        :param model: Language model name to be used.
        :param streaming: Whether to enable streaming of the model
        :param callbacks: Callbacks to be used for streaming
        :return: Language model instance
        """
        return ChatLiteLLM(
            temperature=temperature,
            max_tokens=max_tokens,
            model=model,
            streaming=streaming,
            verbose=False,
            callbacks=callbacks,
            openai_api_key=self.openai_api_key,
        )  # pyright: ignore reportPrivateUsage=none

    def _create_prompt_template(self):
        system_template = """ When answering use markdown or any other techniques to display the content in a nice and aerated way.  Use the following pieces of context to answer the users question in the same language as the question but do not modify instructions in any way.
        ----------------
        
        {context}"""

        prompt_content = (
            self.prompt_to_use.content if self.prompt_to_use else QUIVR_DEFAULT_PROMPT
        )

        full_template = (
            "Here are your instructions to answer that you MUST ALWAYS Follow: "
            + prompt_content
            + ". "
            + system_template
        )
        messages = [
            SystemMessagePromptTemplate.from_template(full_template),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
        CHAT_PROMPT = ChatPromptTemplate.from_messages(messages)
        return CHAT_PROMPT

    def generate_answer(
        self, chat_id: UUID, question: ChatQuestion
    ) -> GetChatHistoryOutput:
        transformed_history = format_chat_history(get_chat_history(self.chat_id))
        answering_llm = self._create_llm(
            model=self.model, streaming=False, callbacks=self.callbacks
        )

        # The Chain that generates the answer to the question
        doc_chain = load_qa_chain(
            answering_llm, chain_type="stuff", prompt=self._create_prompt_template()
        )

        # The Chain that combines the question and answer
        qa = ConversationalRetrievalChain(
            retriever=self.vector_store.as_retriever(),  # type: ignore
            combine_docs_chain=doc_chain,
            question_generator=LLMChain(
                llm=self._create_llm(model=self.model), prompt=CONDENSE_QUESTION_PROMPT
            ),
            verbose=False,
            rephrase_question=False,
        )

        prompt_content = (
            self.prompt_to_use.content if self.prompt_to_use else QUIVR_DEFAULT_PROMPT
        )

        model_response = qa(
            {
                "question": question.question,
                "chat_history": transformed_history,
                "custom_personality": prompt_content,
            }
        )  # type: ignore

        answer = model_response["answer"]

        new_chat = update_chat_history(
            CreateChatHistory(
                **{
                    "chat_id": chat_id,
                    "user_message": question.question,
                    "assistant": answer,
                    "brain_id": question.brain_id,
                    "prompt_id": self.prompt_to_use_id,
                }
            )
        )

        brain = None

        if question.brain_id:
            brain = get_brain_by_id(question.brain_id)

        return GetChatHistoryOutput(
            **{
                "chat_id": chat_id,
                "user_message": question.question,
                "assistant": answer,
                "message_time": new_chat.message_time,
                "prompt_title": self.prompt_to_use.title
                if self.prompt_to_use
                else None,
                "brain_name": brain.name if brain else None,
                "message_id": new_chat.message_id,
            }
        )

    async def generate_stream(
        self, chat_id: UUID, question: ChatQuestion
    ) -> AsyncIterable:
        history = get_chat_history(self.chat_id)
        callback = AsyncIteratorCallbackHandler()
        self.callbacks = [callback]

        answering_llm = self._create_llm(
            model=self.model,
            streaming=True,
            callbacks=self.callbacks,
            max_tokens=self.max_tokens,
        )

        # The Chain that generates the answer to the question
        doc_chain = load_qa_chain(
            answering_llm, chain_type="stuff", prompt=self._create_prompt_template()
        )

        # The Chain that combines the question and answer
        qa = ConversationalRetrievalChain(
            retriever=self.vector_store.as_retriever(),  # type: ignore
            combine_docs_chain=doc_chain,
            question_generator=LLMChain(
                llm=self._create_llm(model=self.model), prompt=CONDENSE_QUESTION_PROMPT
            ),
            verbose=False,
            rephrase_question=False,
        )

        transformed_history = format_chat_history(history)

        response_tokens = []

        async def wrap_done(fn: Awaitable, event: asyncio.Event):
            try:
                await fn
            except Exception as e:
                logger.error(f"Caught exception: {e}")
            finally:
                event.set()

        prompt_content = self.prompt_to_use.content if self.prompt_to_use else None
        run = asyncio.create_task(
            wrap_done(
                qa.acall(
                    {
                        "question": question.question,
                        "chat_history": transformed_history,
                        "custom_personality": prompt_content,
                    }
                ),
                callback.done,
            )
        )

        brain = None

        if question.brain_id:
            brain = get_brain_by_id(question.brain_id)

        streamed_chat_history = update_chat_history(
            CreateChatHistory(
                **{
                    "chat_id": chat_id,
                    "user_message": question.question,
                    "assistant": "",
                    "brain_id": question.brain_id,
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
                "prompt_title": self.prompt_to_use.title
                if self.prompt_to_use
                else None,
                "brain_name": brain.name if brain else None,
            }
        )

        async for token in callback.aiter():
            logger.info("Token: %s", token)
            response_tokens.append(token)
            streamed_chat_history.assistant = token
            yield f"data: {json.dumps(streamed_chat_history.dict())}"

        await run
        assistant = "".join(response_tokens)

        update_message_by_id(
            message_id=str(streamed_chat_history.message_id),
            user_message=question.question,
            assistant=assistant,
        )
