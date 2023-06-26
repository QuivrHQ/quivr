from typing import Any, Dict

# Importing various modules and classes from a custom library 'langchain' likely used for natural language processing
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import GPT4All
from langchain.llms.base import LLM
from langchain.memory import ConversationBufferMemory
from llm.brainpicking import BrainPicking
from llm.prompt.CONDENSE_PROMPT import CONDENSE_QUESTION_PROMPT
from logger import get_logger
from models.settings import BrainSettings  # Importing settings related to the 'brain'
from models.settings import LLMSettings  # For type hinting
from pydantic import BaseModel  # For data validation and settings management
from repository.chat.get_chat_history import get_chat_history
from supabase import Client  # For interacting with Supabase database
from supabase import create_client
from vectorstore.supabase import (
    CustomSupabaseVectorStore,
)  # Custom class for handling vector storage with Supabase

logger = get_logger(__name__)


class PrivateBrainPicking(BrainPicking):
    """
    This subclass of BrainPicking is used to specifically work with a private language model.
    """

    def __init__(
        self,
        model: str,
        user_id: str,
        chat_id: str,
        temperature: float,
        max_tokens: int,
        user_openai_api_key: str,
    ) -> "PrivateBrainPicking":
        """
        Initialize the PrivateBrainPicking class by calling the parent class's initializer.
        :param model: Language model name to be used.
        :param user_id: The user id to be used for CustomSupabaseVectorStore.
        :return: PrivateBrainPicking instance
        """
        # Call the parent class's initializer
        super().__init__(
            model=model,
            user_id=user_id,
            chat_id=chat_id,
            max_tokens=max_tokens,
            temperature=temperature,
            user_openai_api_key=user_openai_api_key,
        )

    def _determine_llm(
        self, private_model_args: dict, private: bool = True, model_name: str = None
    ) -> LLM:
        """
        Override the _determine_llm method to enforce the use of a private model.
        :param model_name: Language model name to be used.
        :param private_model_args: Dictionary containing model_path, n_ctx and n_batch.
        :param private: Boolean value to determine if private model is to be used. Defaulted to True.
        :return: Language model instance
        """
        # Force the use of a private model by setting private to True.
        model_path = private_model_args["model_path"]
        model_n_ctx = private_model_args["n_ctx"]
        model_n_batch = private_model_args["n_batch"]

        logger.info("Using private model: %s", model_path)

        return GPT4All(
            model=model_path,
            n_ctx=model_n_ctx,
            n_batch=model_n_batch,
            backend="gptj",
            verbose=True,
        )
