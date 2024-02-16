from operator import itemgetter
from typing import Optional
from uuid import UUID

from langchain.chains import ConversationalRetrievalChain
from langchain.embeddings.ollama import OllamaEmbeddings
from langchain.llms.base import BaseLLM
from langchain.memory import ConversationBufferMemory
from langchain.prompts import HumanMessagePromptTemplate
from langchain.schema import format_document
from langchain_community.chat_models import ChatLiteLLM
from langchain_core.messages import SystemMessage, get_buffer_string
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from llm.utils.get_prompt_to_use import get_prompt_to_use
from logger import get_logger
from models import BrainSettings  # Importing settings related to the 'brain'
from modules.brain.service.brain_service import BrainService
from modules.chat.service.chat_service import ChatService
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings
from supabase.client import Client, create_client
from vectorstore.supabase import CustomSupabaseVectorStore

logger = get_logger(__name__)


# First step is to create the Rephrasing Prompt
_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

# Next is the answering prompt

template_answer = """
Context:
{context}

User Instructions to follow when answering, default to none: {custom_instructions}
User Question: {question}
Answer:
"""
ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                "When answering use markdown or any other techniques to display the content in a nice and aerated way.  Use the following pieces of context from files provided by the user to answer the users question in the same language as the user question. Your name is Quivr. You're a helpful assistant.  If you don't know the answer with the context provided from the files, just say that you don't know, don't try to make up an answer."
            )
        ),
        HumanMessagePromptTemplate.from_template(template_answer),
    ]
)


# How we format documents

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(
    template="File: {file_name} Content:  {page_content}"
)


def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test


brain_service = BrainService()
chat_service = ChatService()


class QuivrRAG(BaseModel):
    """
    Quivr implementation of the RAGInterface.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Instantiate settings
    brain_settings: BaseSettings = BrainSettings()

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

    def prompt_to_use(self):
        if self.brain_id and is_valid_uuid(self.brain_id):
            return get_prompt_to_use(UUID(self.brain_id), self.prompt_id)
        else:
            return None

    supabase_client: Optional[Client] = None
    vector_store: Optional[CustomSupabaseVectorStore] = None
    qa: Optional[ConversationalRetrievalChain] = None
    prompt_id: Optional[UUID] = None

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

    def _combine_documents(
        self, docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
    ):
        doc_strings = [format_document(doc, document_prompt) for doc in docs]
        return document_separator.join(doc_strings)

    def get_retriever(self):
        return self.vector_store.as_retriever()

    def get_chain(self):
        retriever_doc = self.get_retriever()
        memory = ConversationBufferMemory(
            return_messages=True, output_key="answer", input_key="question"
        )

        loaded_memory = RunnablePassthrough.assign(
            chat_history=RunnableLambda(memory.load_memory_variables)
            | itemgetter("history"),
        )

        standalone_question = {
            "standalone_question": {
                "question": lambda x: x["question"],
                "chat_history": lambda x: get_buffer_string(x["chat_history"]),
            }
            | CONDENSE_QUESTION_PROMPT
            | ChatLiteLLM(temperature=0, model=self.model)
            | StrOutputParser(),
        }

        prompt_custom_user = self.prompt_to_use()
        prompt_to_use = "None"
        if prompt_custom_user:
            prompt_to_use = prompt_custom_user.content

        # Now we retrieve the documents
        retrieved_documents = {
            "docs": itemgetter("standalone_question") | retriever_doc,
            "question": lambda x: x["standalone_question"],
            "custom_instructions": lambda x: prompt_to_use,
        }

        final_inputs = {
            "context": lambda x: self._combine_documents(x["docs"]),
            "question": itemgetter("question"),
            "custom_instructions": itemgetter("custom_instructions"),
        }

        # And finally, we do the part that returns the answers
        answer = {
            "answer": final_inputs
            | ANSWER_PROMPT
            | ChatLiteLLM(max_tokens=self.max_tokens, model=self.model),
            "docs": itemgetter("docs"),
        }

        return loaded_memory | standalone_question | retrieved_documents | answer
