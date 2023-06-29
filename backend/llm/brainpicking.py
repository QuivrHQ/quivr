import asyncio
import json
from typing import AsyncIterable, Awaitable

from langchain.callbacks import AsyncIteratorCallbackHandler

# Importing various modules and classes from a custom library 'langchain' likely used for natural language processing
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms.base import LLM
from llm.prompt.CONDENSE_PROMPT import CONDENSE_QUESTION_PROMPT
from logger import get_logger
from models.settings import BrainSettings  # Importing settings related to the 'brain'
from pydantic import BaseModel  # For data validation and settings management
from repository.chat.get_chat_history import get_chat_history
from repository.chat.update_chat_history import update_chat_history
from repository.chat.update_message_by_id import update_message_by_id
from supabase import Client  # For interacting with Supabase database
from supabase import create_client
from vectorstore.supabase import (
    CustomSupabaseVectorStore,
)  # Custom class for handling vector storage with Supabase

logger = get_logger(__name__)


class BrainPicking(BaseModel):
    """
    Main class for the Brain Picking functionality.
    It allows to initialize a Chat model, generate questions and retrieve answers using ConversationalRetrievalChain.
    """

    # Instantiate settings
    settings = BrainSettings()

    # Default class attributes
    llm_name: str = "gpt-3.5-turbo"
    temperature: float = 0.0
    chat_id: str
    max_tokens: int = 256

    # Storage
    supabase_client: Client = None
    vector_store: CustomSupabaseVectorStore = None

    # Language models
    embeddings: OpenAIEmbeddings = None
    question_llm: LLM = None
    doc_llm: LLM = None
    question_generator: LLMChain = None
    doc_chain: LLMChain = None
    qa: ConversationalRetrievalChain = None

    # Streaming
    callback: AsyncIteratorCallbackHandler = None
    streaming: bool = False

    class Config:
        # Allowing arbitrary types for class validation
        arbitrary_types_allowed = True

    def __init__(
        self,
        model: str,
        brain_id: str,
        temperature: float,
        chat_id: str,
        max_tokens: int,
        user_openai_api_key: str,
        streaming: bool = False,
    ) -> "BrainPicking":
        """
        Initialize the BrainPicking class by setting embeddings, supabase client, vector store, language model and chains.
        :param model: Language model name to be used.
        :param user_brain_idid: The brain id to be used for CustomSupabaseVectorStore.
        :return: BrainPicking instance
        """
        super().__init__(
            model=model,
            brain_id=brain_id,
            chat_id=chat_id,
            max_tokens=max_tokens,
            temperature=temperature,
            user_openai_api_key=user_openai_api_key,
        )
        # If user provided an API key, update the settings
        if user_openai_api_key is not None:
            self.settings.openai_api_key = user_openai_api_key

        self.temperature = temperature
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.settings.openai_api_key)
        self.supabase_client = create_client(
            self.settings.supabase_url, self.settings.supabase_service_key
        )
        self.llm_name = model
        self.vector_store = CustomSupabaseVectorStore(
            self.supabase_client,
            self.embeddings,
            table_name="vectors",
            brain_id=brain_id,
        )

        self.question_llm = self._create_llm(
            model_name=self.llm_name,
            streaming=False,
        )
        self.question_generator = LLMChain(
            llm=self.question_llm, prompt=CONDENSE_QUESTION_PROMPT
        )

        if streaming:
            self.callback = AsyncIteratorCallbackHandler()
            self.doc_llm = self._create_llm(
                model_name=self.llm_name,
                streaming=streaming,
                callbacks=[self.callback],
            )
            self.doc_chain = load_qa_chain(
                llm=self.doc_llm,
                chain_type="stuff",
            )
            self.streaming = streaming
        else:
            self.doc_llm = self._create_llm(
                model_name=self.llm_name,
                streaming=streaming,
            )
            self.doc_chain = load_qa_chain(llm=self.doc_llm, chain_type="stuff")
            self.streaming = streaming

        self.chat_id = chat_id
        self.max_tokens = max_tokens

    def _create_llm(self, model_name, streaming=False, callbacks=None) -> LLM:
        """
        Determine the language model to be used.
        :param model_name: Language model name to be used.
        :param private_model_args: Dictionary containing model_path, n_ctx and n_batch.
        :param private: Boolean value to determine if private model is to be used.
        :return: Language model instance
        """
        return ChatOpenAI(
            temperature=0,
            model_name=model_name,
            streaming=streaming,
            callbacks=callbacks,
        )

    def _get_qa(
        self,
    ) -> ConversationalRetrievalChain:
        """
        Retrieves a QA chain for the given chat message and API key.
        :param chat_message: The chat message containing history.
        :param user_openai_api_key: The OpenAI API key to be used.
        :return: ConversationalRetrievalChain instance
        """

        # Initialize and return a ConversationalRetrievalChain
        qa = ConversationalRetrievalChain(
            retriever=self.vector_store.as_retriever(),
            question_generator=self.question_generator,
            combine_docs_chain=self.doc_chain,
            verbose=True,
        )

        return qa

    def generate_answer(self, question: str) -> str:
        """
        Generate an answer to a given question by interacting with the language model.
        :param question: The question
        :return: The generated answer.
        """
        transformed_history = []

        # Get the QA chain
        qa = self._get_qa()
        history = get_chat_history(self.chat_id)

        # Format the chat history into a list of tuples (human, ai)
        transformed_history = [(chat.user_message, chat.assistant) for chat in history]

        # Generate the model response using the QA chain
        model_response = qa({"question": question, "chat_history": transformed_history})
        answer = model_response["answer"]

        return answer

    async def generate_stream(self, question: str) -> AsyncIterable:
        """
        Generate a streaming answer to a given question by interacting with the language model.
        :param question: The question
        :return: An async iterable which generates the answer.
        """

        # Get the QA chain
        qa = self._get_qa()
        history = get_chat_history(self.chat_id)
        callback = self.callback

        # # Format the chat history into a list of tuples (human, ai)
        transformed_history = [(chat.user_message, chat.assistant) for chat in history]

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

        # Use the acall method to perform an async call to the QA chain
        task = asyncio.create_task(
            wrap_done(
                qa.acall(
                    {
                        "question": question,
                        "chat_history": transformed_history,
                    }
                ),
                callback.done,
            )
        )

        streamed_chat_history = update_chat_history(
            chat_id=self.chat_id,
            user_message=question,
            assistant="",
        )

        # Use the aiter method of the callback to stream the response with server-sent-events
        async for token in callback.aiter():
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
