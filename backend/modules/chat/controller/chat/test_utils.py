# FILEPATH: /Users/stan/Dev/Padok/secondbrain/backend/modules/chat/controller/chat/test_utils.py

import uuid
from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException
from models.databases.entity import LLMModels
from modules.chat.controller.chat.utils import (
    find_model_and_generate_metadata,
    update_user_usage,
)


@patch("modules.chat.controller.chat.utils.chat_service")
def test_find_model_and_generate_metadata(mock_chat_service):
    chat_id = uuid.uuid4()
    brain = Mock()
    brain.model = "gpt-3.5-turbo-0125"
    user_settings = {"models": ["gpt-3.5-turbo-0125"]}
    models_settings = [
        {"name": "gpt-3.5-turbo-0125", "max_input": 512, "max_output": 512}
    ]
    metadata_brain = {"key": "value"}

    mock_chat_service.get_follow_up_question.return_value = []

    model_to_use, metadata = find_model_and_generate_metadata(
        chat_id, brain, user_settings, models_settings, metadata_brain
    )

    assert isinstance(model_to_use, LLMModels)
    assert model_to_use.name == "gpt-3.5-turbo-0125"
    assert model_to_use.max_input == 512
    assert model_to_use.max_output == 512
    assert metadata == {
        "key": "value",
        "follow_up_questions": [],
        "model": "gpt-3.5-turbo-0125",
        "max_tokens": 512,
        "max_input": 512,
    }


@patch("modules.chat.controller.chat.utils.chat_service")
def test_find_model_and_generate_metadata_user_not_allowed(mock_chat_service):
    chat_id = uuid.uuid4()
    brain = Mock()
    brain.model = "gpt-3.5-turbo-0125"
    user_settings = {
        "models": ["gpt-3.5-turbo-1107"]
    }  # User is not allowed to use the brain's model
    models_settings = [
        {"name": "gpt-3.5-turbo-0125", "max_input": 512, "max_output": 512},
        {"name": "gpt-3.5-turbo-1107", "max_input": 12000, "max_output": 12000},
    ]
    metadata_brain = {"key": "value"}

    mock_chat_service.get_follow_up_question.return_value = []

    model_to_use, metadata = find_model_and_generate_metadata(
        chat_id, brain, user_settings, models_settings, metadata_brain
    )

    assert isinstance(model_to_use, LLMModels)
    assert model_to_use.name == "gpt-3.5-turbo-0125"  # Default model is used
    assert model_to_use.max_input == 12000
    assert model_to_use.max_output == 1000
    assert metadata == {
        "key": "value",
        "follow_up_questions": [],
        "model": "gpt-3.5-turbo-0125",
        "max_tokens": 1000,
        "max_input": 12000,
    }


@patch("modules.chat.controller.chat.utils.time")
def test_check_update_user_usage_within_limit(mock_time):
    mock_time.strftime.return_value = "20220101"
    usage = Mock()
    usage.get_user_monthly_usage.return_value = 50
    user_settings = {"monthly_chat_credit": 100}
    models_settings = [{"name": "gpt-3.5-turbo", "price": 10}]
    model_name = "gpt-3.5-turbo"

    update_user_usage(usage, user_settings, models_settings, model_name)

    usage.handle_increment_user_request_count.assert_called_once_with("20220101", 10)


@patch("modules.chat.controller.chat.utils.time")
def test_update_user_usage_exceeds_limit(mock_time):
    mock_time.strftime.return_value = "20220101"
    usage = Mock()
    usage.get_user_monthly_usage.return_value = 100
    user_settings = {"monthly_chat_credit": 100}
    models_settings = [{"name": "gpt-3.5-turbo", "price": 10}]
    model_name = "gpt-3.5-turbo"

    with pytest.raises(HTTPException) as exc_info:
        update_user_usage(usage, user_settings, models_settings, model_name)

    assert exc_info.value.status_code == 429
    assert (
        "You have reached your monthly chat limit of 100 requests per months."
        in str(exc_info.value.detail)
    )
