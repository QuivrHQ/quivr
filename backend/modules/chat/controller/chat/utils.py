import time
from uuid import UUID

from fastapi import HTTPException
from logger import get_logger
from models import UserUsage
from models.databases.entity import LLMModels
from modules.brain.service.brain_service import BrainService
from modules.chat.service.chat_service import ChatService

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
    brain,
    user_settings,
    models_settings,
    metadata_brain,
):
    # Add metadata_brain to metadata
    metadata = {}
    metadata = {**metadata, **metadata_brain}
    follow_up_questions = chat_service.get_follow_up_question(chat_id)
    metadata["follow_up_questions"] = follow_up_questions
    # Default model is gpt-3.5-turbo-0125
    default_model = "gpt-3.5-turbo-0125"
    model_to_use = LLMModels(  # TODO Implement default models in database
        name=default_model, price=1, max_input=4000, max_output=1000
    )

    logger.info("Brain model: %s", brain.model)

    # If brain.model is None, set it to the default_model
    if brain.model is None:
        brain.model = default_model

    is_brain_model_available = any(
        brain.model == model_dict.get("name") for model_dict in models_settings
    )

    is_user_allowed_model = brain.model in user_settings.get(
        "models", [default_model]
    )  # Checks if the model is available in the list of models

    logger.info(f"Brain model: {brain.model}")
    logger.info(f"User models: {user_settings.get('models', [])}")
    logger.info(f"Model available: {is_brain_model_available}")
    logger.info(f"User allowed model: {is_user_allowed_model}")

    if is_brain_model_available and is_user_allowed_model:
        # Use the model from the brain
        model_to_use.name = brain.model
        for model_dict in models_settings:
            if model_dict.get("name") == model_to_use.name:
                model_to_use.price = model_dict.get("price")
                model_to_use.max_input = model_dict.get("max_input")
                model_to_use.max_output = model_dict.get("max_output")
                break

    metadata["model"] = model_to_use.name
    metadata["max_tokens"] = model_to_use.max_output
    metadata["max_input"] = model_to_use.max_input

    logger.info(f"Model to use: {model_to_use}")
    logger.info(f"Metadata: {metadata}")

    return model_to_use, metadata


def check_user_requests_limit(
    usage: UserUsage, user_settings, models_settings, model_name: str
):
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
    daily_user_count = usage.get_user_monthly_usage(date)
    user_choosen_model_price = 1000

    for model_setting in models_settings:
        if model_setting["name"] == model_name:
            user_choosen_model_price = model_setting["price"]

    if int(daily_user_count + user_choosen_model_price) > int(monthly_chat_credit):
        raise HTTPException(
            status_code=429,  # pyright: ignore reportPrivateUsage=none
            detail=f"You have reached your monthly chat limit of {monthly_chat_credit} requests per months. Please upgrade your plan to increase your daily chat limit.",
        )
    else:
        usage.handle_increment_user_request_count(date, user_choosen_model_price)
        pass
