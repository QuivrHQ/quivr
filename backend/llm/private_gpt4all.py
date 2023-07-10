from langchain.llms.base import LLM
from langchain.llms.gpt4all import GPT4All
from logger import get_logger
from models.settings import LLMSettings

from .base import BaseBrainPicking

logger = get_logger(__name__)


class PrivateGPT4AllBrainPicking(BaseBrainPicking):
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

        # set defaults
        model = "gpt4all-j-1.3"

        super().__init__(
            model=model,
            brain_id=brain_id,
            chat_id=chat_id,
            streaming=streaming,
        )

    def _create_llm(self) -> LLM:
        """
        Override the _create_llm method to enforce the use of a private model.
        :return: Language model instance
        """
        model_path = self.llm_settings.model_path
        model_n_ctx = self.llm_settings.model_n_ctx
        model_n_batch = self.llm_settings.model_n_batch

        logger.info("Using private model: %s", model_path)

        return GPT4All(
            model=model_path,
            n_ctx=model_n_ctx,
            n_batch=model_n_batch,
            backend="gptj",
            verbose=True,
        )  # pyright: ignore reportPrivateUsage=none
