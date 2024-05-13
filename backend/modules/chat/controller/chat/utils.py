import time
from uuid import UUID

from fastapi import HTTPException
from logger import get_logger
from models.databases.llm_models import LLMModels
from modules.brain.service.brain_service import BrainService
from modules.chat.service.chat_service import ChatService
from modules.user.service.user_usage import UserUsage

logger = get_logger(__name__)
brain_service = BrainService()
chat_service = ChatService()


class NullableUUID(UUID):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(v, values, **kwargs):
        logger.info(f"Validating UUID: {v}")
        if v == "":
            return None
        try:
            return UUID(v)
        except ValueError:
            return None


def find_model_and_generate_metadata(
    chat_id: UUID,
    brain_model: str,
    user_settings,
    models_settings,
):

    # Default model is gpt-3.5-turbo-0125
    default_model = "gpt-3.5-turbo-0125"
    model_to_use = LLMModels(  # TODO Implement default models in database
        name=default_model, price=1, max_input=4000, max_output=1000
    )

    logger.debug("Brain model: %s", brain_model)

    # If brain.model is None, set it to the default_model
    if brain_model is None:
        brain_model = default_model

    is_brain_model_available = any(
        brain_model == model_dict.get("name") for model_dict in models_settings
    )

    is_user_allowed_model = brain_model in user_settings.get(
        "models", [default_model]
    )  # Checks if the model is available in the list of models

    logger.debug(f"Brain model: {brain_model}")
    logger.debug(f"User models: {user_settings.get('models', [])}")
    logger.debug(f"Model available: {is_brain_model_available}")
    logger.debug(f"User allowed model: {is_user_allowed_model}")

    if is_brain_model_available and is_user_allowed_model:
        # Use the model from the brain
        model_to_use.name = brain_model
        for model_dict in models_settings:
            if model_dict.get("name") == model_to_use.name:
                model_to_use.price = model_dict.get("price")
                model_to_use.max_input = model_dict.get("max_input")
                model_to_use.max_output = model_dict.get("max_output")
                break

    logger.info(f"Model to use: {model_to_use}")

    return model_to_use


def update_user_usage(usage: UserUsage, user_settings, cost: int = 100):
    """Checks the user requests limit.
    It checks the user requests limit and raises an exception if the user has reached the limit.
    By default, the user has a limit of 100 requests per month. The limit can be increased by upgrading the plan.

    Args:
        user (UserIdentity): User object
        model (str): Model name for which the user is making the request

    Raises:
        HTTPException: Raises a 429 error if the user has reached the limit.
    """
    usage

    date = time.strftime("%Y%m%d")

    monthly_chat_credit = user_settings.get("monthly_chat_credit", 100)
    montly_usage = usage.get_user_monthly_usage(date)

    if int(montly_usage + cost) > int(monthly_chat_credit):
        raise HTTPException(
            status_code=429,  # pyright: ignore reportPrivateUsage=none
            detail=f"You have reached your monthly chat limit of {monthly_chat_credit} requests per months. Please upgrade your plan to increase your monthly chat limit.",
        )
    else:
        usage.handle_increment_user_request_count(date, cost)
        pass
