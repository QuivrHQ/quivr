
# Importing various modules and classes from a custom library 'langchain' likely used for natural language processing
from langchain.llms import GPT4All
from langchain.llms.base import LLM
from llm.brainpicking import BrainPicking
from logger import get_logger

logger = get_logger(__name__)


class PrivateBrainPicking(BrainPicking):
    """
    This subclass of BrainPicking is used to specifically work with a private language model.
    """

    def __init__(
        self,
        model: str,
        chat_id: str,
        brain_id:str,
        temperature: float,
        max_tokens: int,
        user_openai_api_key: str,
    ) -> "PrivateBrainPicking":
        """
        Initialize the PrivateBrainPicking class by calling the parent class's initializer.
        :param model: Language model name to be used.
        :param brain_id: The user id to be used for CustomSupabaseVectorStore.
        :return: PrivateBrainPicking instance
        """
        # Call the parent class's initializer
        super().__init__(
            model=model,
            brain_id=brain_id,
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
