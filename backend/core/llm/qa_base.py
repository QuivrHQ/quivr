import asyncio
import json
from abc import abstractmethod, abstractproperty
from typing import AsyncIterable, Awaitable

from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms.base import BaseLLM
from logger import get_logger
from models.chat import ChatHistory
from repository.chat.format_chat_history import format_chat_history
from repository.chat.get_chat_history import get_chat_history
from repository.chat.update_chat_history import update_chat_history
from repository.chat.update_message_by_id import update_message_by_id
from supabase.client import Client, create_client
from vectorstore.supabase import CustomSupabaseVectorStore

from .base import BaseBrainPicking
from .prompts.CONDENSE_PROMPT import CONDENSE_QUESTION_PROMPT

logger = get_logger(__name__)


class QABaseBrainPicking(BaseBrainPicking):
    """
    Base class for the Brain Picking functionality using the Conversational Retrieval Chain (QA) from Langchain.
    It is not designed to be used directly, but to be subclassed by other classes which use the QA chain.
    """

    def __init__(
        self,
        model: str,
        brain_id: str,
        chat_id: str,
        streaming: bool = False,
        **kwargs,
    ) -> "QABaseBrainPicking":  # pyright: ignore reportPrivateUsage=none
        """
        Initialize the QA BrainPicking class by setting embeddings, supabase client, vector store, language model and chains.
        :return: QABrainPicking instance
        """
        super().__init__(
            model=model,
            brain_id=brain_id,
            chat_id=chat_id,
            streaming=streaming,
            **kwargs,
        )

    @abstractproperty
    def embeddings(self) -> OpenAIEmbeddings:
        raise NotImplementedError("This property should be overridden in a subclass.")

    @property
    def supabase_client(self) -> Client:
        return create_client(
            self.brain_settings.supabase_url, self.brain_settings.supabase_service_key
        )

    @property
    def vector_store(self) -> CustomSupabaseVectorStore:
        return CustomSupabaseVectorStore(
            self.supabase_client,
            self.embeddings,
            table_name="vectors",
            brain_id=self.brain_id,
        )

    @property
    def question_llm(self):
        return self._create_llm(model=self.model, streaming=False)

    @property
    def doc_llm(self):
        return self._create_llm(
            model=self.model, streaming=self.streaming, callbacks=self.callbacks
        )

    @property
    def question_generator(self) -> LLMChain:
        return LLMChain(llm=self.question_llm, prompt=CONDENSE_QUESTION_PROMPT)

    @property
    def doc_chain(self) -> LLMChain:
        return load_qa_chain(
            llm=self.doc_llm, chain_type="stuff"
        )  # pyright: ignore reportPrivateUsage=none

    @property
    def qa(self) -> ConversationalRetrievalChain:
        return ConversationalRetrievalChain(
            retriever=self.vector_store.as_retriever(),
            question_generator=self.question_generator,
            combine_docs_chain=self.doc_chain,  # pyright: ignore reportPrivateUsage=none
            verbose=True,
        )

    @abstractmethod
    def _create_llm(self, model, streaming=False, callbacks=None) -> BaseLLM:
        """
        Determine the language model to be used.
        :param model: Language model name to be used.
        :param streaming: Whether to enable streaming of the model
        :param callbacks: Callbacks to be used for streaming
        :return: Language model instance
        """

    def _call_chain(self, chain, question, history):
        """
        Call a chain with a given question and history.
        :param chain: The chain eg QA (ConversationalRetrievalChain)
        :param question: The user prompt
        :param history: The chat history from DB
        :return: The answer.
        """
        return chain(
            {
                "question": question,
                "chat_history": history,
            }
        )

    def generate_answer(self, question: str) -> ChatHistory:
        """
        Generate an answer to a given question by interacting with the language model.
        :param question: The question
        :return: The generated answer.
        """
        transformed_history = []

        # Get the history from the database
        history = get_chat_history(self.chat_id)

        # Format the chat history into a list of tuples (human, ai)
        transformed_history = format_chat_history(history)

        # Generate the model response using the QA chain
        model_response = self._call_chain(self.qa, question, transformed_history)

        answer = model_response["answer"]

        # Update chat history
        chat_answer = update_chat_history(
            chat_id=self.chat_id,
            user_message=question,
            assistant=answer,
        )

        return chat_answer

    async def _acall_chain(self, chain, question, history):
        """
        Call a chain with a given question and history.
        :param chain: The chain eg QA (ConversationalRetrievalChain)
        :param question: The user prompt
        :param history: The chat history from DB
        :return: The answer.
        """
        return chain.acall(
            {
                "question": question,
                "chat_history": history,
            }
        )

    async def generate_stream(self, question: str) -> AsyncIterable:
        """
        Generate a streaming answer to a given question by interacting with the language model.
        :param question: The question
        :return: An async iterable which generates the answer.
        """

        history = get_chat_history(self.chat_id)
        callback = self.callbacks[0]

        transformed_history = []

        # Format the chat history into a list of tuples (human, ai)
        transformed_history = format_chat_history(history)

        # Initialize a list to hold the tokens
        response_tokens = []

        # Wrap an awaitable with a event to signal when it's done or an exception is raised.
        async def wrap_done(fn: Awaitable, event: asyncio.Event):
            try:
                await fn
            except Exception as e:
                logger.error(f"Caught exception: {e}")
            finally:
                event.set()

        task = asyncio.create_task(
            wrap_done(
                self.qa._acall_chain(  # pyright: ignore reportPrivateUsage=none
                    self.qa, question, transformed_history
                ),
                callback.done,  # pyright: ignore reportPrivateUsage=none
            )
        )

        streamed_chat_history = update_chat_history(
            chat_id=self.chat_id,
            user_message=question,
            assistant="",
        )

        # Use the aiter method of the callback to stream the response with server-sent-events
        async for token in callback.aiter():  # pyright: ignore reportPrivateUsage=none
            logger.info("Token: %s", token)

            # Add the token to the response_tokens list
            response_tokens.append(token)
            streamed_chat_history.assistant = token

            yield f"data: {json.dumps(streamed_chat_history.to_dict())}"

        await task

        # Join the tokens to create the assistant's response
        assistant = "".join(response_tokens)

        update_message_by_id(
            message_id=streamed_chat_history.message_id,
            user_message=question,
            assistant=assistant,
        )
