import uuid

import pytest
from fastapi import HTTPException
from modules.prompt.repository.prompts import Prompts


def test_get_public_prompts(client, api_key):
    response = client.get(
        "/prompts",
        headers={"Authorization": "Bearer " + api_key},
    )
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_delete_prompt_by_id_not_found():
    # Arrange
    prompts = Prompts()
    prompt_id = uuid.uuid4()  # Generate a valid UUID

    # Act and Assert
    with pytest.raises(HTTPException) as exc_info:
        prompts.delete_prompt_by_id(prompt_id)

    assert exc_info.value.status_code == 404
    assert str(exc_info.value.detail) == "Prompt not found"
