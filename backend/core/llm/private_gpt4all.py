from typing import Optional

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms.base import BaseLLM
from langchain.llms.gpt4all import GPT4All
from llm.qa_base import QABaseBrainPicking
from logger import get_logger

logger = get_logger(__name__)


class PrivateGPT4AllBrainPicking(QABaseBrainPicking):
    """
    This subclass of BrainPicking is used to specifically work with the private language model GPT4All.
    """

    # Define the default model path
    model_path: str = "./local_models/ggml-gpt4all-j-v1.3-groovy.bin"

    def __init__(
        self,
        chat_id: str,
        brain_id: str,
        user_openai_api_key: Optional[str],
        streaming: bool,
        model_path: str,
    ) -> None:
        """
        Initialize the PrivateBrainPicking class by calling the parent class's initializer.
        :param brain_id: The brain_id in the DB.
        :param chat_id: The id of the chat in the DB.
        :param streaming: Whether to enable streaming of the model
        :param model_path: The path to the model. If not provided, a default path is used.
        """

        super().__init__(
            model="gpt4all-j-1.3",
            brain_id=brain_id,
            chat_id=chat_id,
            user_openai_api_key=user_openai_api_key,
            streaming=streaming,
        )

        # Set the model path
        self.model_path = model_path

    # TODO: Use private embeddings model. This involves some restructuring of how we store the embeddings.
    @property
    def embeddings(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(
            openai_api_key=self.openai_api_key
        )  # pyright: ignore reportPrivateUsage=none

    def _create_llm(
        self,
        model,
        streaming=False,
        callbacks=None,
    ) -> BaseLLM:
        """
        Override the _create_llm method to enforce the use of a private model.
        :param model: Language model name to be used.
        :param streaming: Whether to enable streaming of the model
        :param callbacks: Callbacks to be used for streaming
        :return: Language model instance
        """
        model_path = self.model_path

        logger.info("Using private model: %s", model)
        logger.info("Streaming is set to %s", streaming)

        return GPT4All(
            model=model_path,
        )  # pyright: ignore reportPrivateUsage=none
