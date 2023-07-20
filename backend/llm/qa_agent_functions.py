import logging

from .qa_base import QABaseBrainPicking
from langchain import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms.base import BaseLLM
from supabase.client import Client, create_client
from vectorstore.supabase import CustomSupabaseVectorStore


logger = logging.getLogger(__name__)

"""
- class for QA answer agent that understand arabic language,
- format the answer to be clean no brock arabic text,
- use ChatOpenai to use functions and gpt-4 model,
- connected to the What's app business,  
"""


class AgentFunctionsQA(QABaseBrainPicking):
    """
        Class for the OpenAI Brain Picking functionality using OpenAI Functions.
        It allows to initialize a Chat model, generate questions and retrieve answers using ConversationalRetrievalChain.
        """

    # Default class attributes
    model: str = "gpt-3.5-turbo-0613"

    def __init__(
            self,
            model: str,
            chat_id: str,
            temperature: float,
            max_tokens: int,
            brain_id: str,
            user_openai_api_key: str,
            streaming: bool
    ) -> "AgentFunctionsQA":  # pyright: ignore reportPrivateUsage=none
        super().__init__(
            model=model,
            chat_id=chat_id,
            max_tokens=max_tokens,
            user_openai_api_key=user_openai_api_key,
            temperature=temperature,
            brain_id=str(brain_id),
            streaming=False,
        )

    @property
    def embeddings(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(
            openai_api_key=self.openai_api_key
        )  # pyright: ignore reportPrivateUsage=none

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

    def _create_llm(self, model, streaming=False, callbacks=None) -> BaseLLM:
        pass

