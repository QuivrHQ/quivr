from langchain.embeddings.openai import OpenAIEmbeddings
from llm.qa_base import QABaseBrainPicking
from logger import get_logger

logger = get_logger(__name__)


class OpenAIBrainPicking(QABaseBrainPicking):
    """
    Main class for the OpenAI Brain Picking functionality.
    It allows to initialize a Chat model, generate questions and retrieve answers using ConversationalRetrievalChain.
    """

    # Default class attributes
    model: str = "gpt-3.5-turbo"

    def __init__(
        self,
        model: str,
        brain_id: str,
        temperature: float,
        chat_id: str,
        max_tokens: int,
        user_openai_api_key: str,
        streaming: bool = False,
    ) -> "OpenAIBrainPicking":  # pyright: ignore reportPrivateUsage=none
        """
        Initialize the BrainPicking class by setting embeddings, supabase client, vector store, language model and chains.
        :return: OpenAIBrainPicking instance
        """
        super().__init__(
            model=model,
            brain_id=brain_id,
            chat_id=chat_id,
            max_tokens=max_tokens,
            temperature=temperature,
            user_openai_api_key=user_openai_api_key,
            streaming=streaming,
        )

    @property
    def embeddings(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(
            openai_api_key=self.openai_api_key
        )  # pyright: ignore reportPrivateUsage=none

    
