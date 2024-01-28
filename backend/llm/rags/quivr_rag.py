from typing import Optional
from uuid import UUID

from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatLiteLLM
from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms.base import BaseLLM
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from llm.rags.rag_interface import RAGInterface
from llm.utils.get_prompt_to_use import get_prompt_to_use
from logger import get_logger
from models import BrainSettings  # Importing settings related to the 'brain'
from modules.brain.service.brain_service import BrainService
from modules.chat.service.chat_service import ChatService
from pydantic import BaseModel
from supabase.client import Client, create_client
from vectorstore.supabase import CustomSupabaseVectorStore

from ..prompts.CONDENSE_PROMPT import CONDENSE_QUESTION_PROMPT

logger = get_logger(__name__)
QUIVR_DEFAULT_PROMPT = "Your name is Quivr. You're a helpful assistant.  If you don't know the answer, just say that you don't know, don't try to make up an answer."


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test


brain_service = BrainService()
chat_service = ChatService()


class QuivrRAG(BaseModel, RAGInterface):
    """
    Quivr implementation of the RAGInterface.
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
    max_tokens: int = 2000  # Output length
    max_input: int = 2000
    streaming: bool = False

    @property
    def embeddings(self):
        if self.brain_settings.ollama_api_base_url:
            return OllamaEmbeddings(
                base_url=self.brain_settings.ollama_api_base_url
            )  # pyright: ignore reportPrivateUsage=none
        else:
            return OpenAIEmbeddings()

    @property
    def prompt_to_use(self):
        if self.brain_id and is_valid_uuid(self.brain_id):
            return get_prompt_to_use(UUID(self.brain_id), self.prompt_id)
        else:
            return None

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
        max_tokens: int = 2000,
        max_input: int = 2000,
        **kwargs,
    ):
        super().__init__(
            model=model,
            brain_id=brain_id,
            chat_id=chat_id,
            streaming=streaming,
            max_tokens=max_tokens,
            max_input=max_input,
            **kwargs,
        )
        self.supabase_client = self._create_supabase_client()
        self.vector_store = self._create_vector_store()
        self.prompt_id = prompt_id
        self.max_tokens = max_tokens
        self.max_input = max_input
        self.model = model
        self.brain_id = brain_id
        self.chat_id = chat_id
        self.streaming = streaming

        logger.info(f"QuivrRAG initialized with model {model} and brain {brain_id}")
        logger.info("Max input length: " + str(self.max_input))

    def _create_supabase_client(self) -> Client:
        return create_client(
            self.brain_settings.supabase_url, self.brain_settings.supabase_service_key
        )

    def _create_vector_store(self) -> CustomSupabaseVectorStore:
        return CustomSupabaseVectorStore(
            self.supabase_client,
            self.embeddings,
            table_name="vectors",
            brain_id=self.brain_id,
            max_input=self.max_input,
        )

    def _create_llm(
        self,
        callbacks,
        model,
        streaming=False,
        temperature=0,
    ) -> BaseLLM:
        """
        Create a LLM with the given parameters
        """
        if streaming and callbacks is None:
            raise ValueError(
                "Callbacks must be provided when using streaming language models"
            )

        api_base = None
        if self.brain_settings.ollama_api_base_url and model.startswith("ollama"):
            api_base = self.brain_settings.ollama_api_base_url

        return ChatLiteLLM(
            temperature=temperature,
            max_tokens=self.max_tokens,
            model=model,
            streaming=streaming,
            verbose=False,
            callbacks=callbacks,
            api_base=api_base,
        )

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

    def get_doc_chain(self, streaming, callbacks=None):
        answering_llm = self._create_llm(
            model=self.model,
            callbacks=callbacks,
            streaming=streaming,
        )

        doc_chain = load_qa_chain(
            answering_llm, chain_type="stuff", prompt=self._create_prompt_template()
        )
        return doc_chain

    def get_question_generation_llm(self):
        return LLMChain(
            llm=self._create_llm(model=self.model, callbacks=None),
            prompt=CONDENSE_QUESTION_PROMPT,
            callbacks=None,
        )

    def get_retriever(self):
        return self.vector_store.as_retriever()

    # Some other methods can be added such as on_stream, on_end,... to abstract history management (each answer should be saved or not)    # Some other methods can be added such as on_stream, on_end,... to abstract history management (each answer should be saved or not)
    # Some other methods can be added such as on_stream, on_end,... to abstract history management (each answer should be saved or not)
