from typing import Any, Dict

# Importing various modules and classes from a custom library 'langchain' likely used for natural language processing
from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms.base import LLM
from langchain.memory import ConversationBufferMemory
from llm.prompt.CONDENSE_PROMPT import CONDENSE_QUESTION_PROMPT
from logger import get_logger
from models.settings import \
    BrainSettings  # Importing settings related to the 'brain'
from models.settings import LLMSettings  # For type hinting
from pydantic import BaseModel  # For data validation and settings management
from repository.chat.get_chat_history import get_chat_history
from vectorstore.supabase import \
    CustomSupabaseVectorStore  # Custom class for handling vector storage with Supabase

from supabase import Client  # For interacting with Supabase database
from supabase import create_client

logger = get_logger(__name__)


class AnswerConversationBufferMemory(ConversationBufferMemory):
    """
    This class is a specialized version of ConversationBufferMemory.
    It overrides the save_context method to save the response using the 'answer' key in the outputs.
    Reference to some issue comment is given in the docstring.
    """

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        # Overriding the save_context method of the parent class
        return super(AnswerConversationBufferMemory, self).save_context(
            inputs, {"response": outputs["answer"]}
        )


def format_chat_history(inputs) -> str:
    """
    Function to concatenate chat history into a single string.
    :param inputs: List of tuples containing human and AI messages.
    :return: concatenated string of chat history
    """
    res = []
    for human, ai in inputs:
        res.append(f"{human}:{ai}\n")
    return "\n".join(res)


class BrainPicking(BaseModel):
    """
    Main class for the Brain Picking functionality.
    It allows to initialize a Chat model, generate questions and retrieve answers using ConversationalRetrievalChain.
    """

    # Default class attributes
    llm_name: str = "gpt-3.5-turbo"
    temperature: float = 0.0
    settings = BrainSettings()
    llm_config = LLMSettings()
    embeddings: OpenAIEmbeddings = None
    supabase_client: Client = None
    vector_store: CustomSupabaseVectorStore = None
    llm: LLM = None
    question_generator: LLMChain = None
    doc_chain: ConversationalRetrievalChain = None
    chat_id: str
    max_tokens: int = 256

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

        self.llm = self._determine_llm(
            private_model_args={
                "model_path": self.llm_config.model_path,
                "n_ctx": self.llm_config.model_n_ctx,
                "n_batch": self.llm_config.model_n_batch,
            },
            private=self.llm_config.private,
            model_name=self.llm_name,
        )
        self.question_generator = LLMChain(
            llm=self.llm, prompt=CONDENSE_QUESTION_PROMPT
        )
        self.doc_chain = load_qa_chain(self.llm, chain_type="stuff")
        self.chat_id = chat_id
        self.max_tokens = max_tokens

    def _determine_llm(
        self, private_model_args: dict, private: bool = False, model_name: str = None
    ) -> LLM:
        """
        Determine the language model to be used.
        :param model_name: Language model name to be used.
        :param private_model_args: Dictionary containing model_path, n_ctx and n_batch.
        :param private: Boolean value to determine if private model is to be used.
        :return: Language model instance
        """

        return ChatOpenAI(temperature=0, model_name=model_name)

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
            max_tokens_limit=self.max_tokens,
            question_generator=self.question_generator,
            combine_docs_chain=self.doc_chain,
            get_chat_history=format_chat_history,
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
