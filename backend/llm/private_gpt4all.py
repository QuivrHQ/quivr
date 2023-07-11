from langchain.llms.base import LLM
from langchain.llms.gpt4all import GPT4All
from llm.openai import OpenAIBrainPicking
from logger import get_logger
from models.settings import LLMSettings

logger = get_logger(__name__)


class PrivateGPT4AllBrainPicking(OpenAIBrainPicking):
    """
    This subclass of BrainPicking is used to specifically work with the private language model GPT4All.
    """

    # Initialize class settings
    llm_settings = LLMSettings()

    def __init__(
        self,
        chat_id: str,
        brain_id: str,
        streaming: bool,
    ) -> "PrivateGPT4AllBrainPicking":  # pyright: ignore reportPrivateUsage=none
        """
        Initialize the PrivateBrainPicking class by calling the parent class's initializer.
        :param brain_id: The brain_id in the DB.
        :param chat_id: The id of the chat in the DB.
        :param streaming: Whether to enable streaming of the model
        :return: PrivateBrainPicking instance
        """

        # set defaults to use the parent class's initializer
        model = "gpt4all-j-1.3"
        user_openai_api_key = ""
        temperature = 0.0
        max_tokens = 256

        super().__init__(
            model=model,
            brain_id=brain_id,
            chat_id=chat_id,
            max_tokens=max_tokens,
            temperature=temperature,
            user_openai_api_key=user_openai_api_key,
            streaming=streaming,
        )

    def _create_llm(
        self,
        model,
        streaming=False,
        callbacks=None,
    ) -> LLM:
        """
        Override the _create_llm method to enforce the use of a private model.
        :return: Language model instance
        """
        model_path = self.llm_settings.model_path

        logger.info("Using private model: %s", model)
        logger.info("Streaming is set to %s", streaming)

        return GPT4All(
            model=model_path,
            backend="gptj",
            verbose=True,
        )  # pyright: ignore reportPrivateUsage=none
