from uuid import UUID

from fastapi import HTTPException
from llm.utils.extract_api_brain_definition_values_from_llm_output import (
    extract_api_brain_definition_values_from_llm_output,
)
from llm.utils.make_api_request import get_api_call_response_as_text
from modules.brain.service.api_brain_definition_service import ApiBrainDefinitionService
from modules.brain.service.brain_service import BrainService

brain_service = BrainService()
api_brain_definition_service = ApiBrainDefinitionService()


def call_brain_api(brain_id: UUID, user_id: UUID, arguments: dict) -> str:
    brain_definition = api_brain_definition_service.get_api_brain_definition(brain_id)

    if brain_definition is None:
        raise HTTPException(
            status_code=404, detail=f"Brain definition {brain_id} not found"
        )

    brain_params_values = extract_api_brain_definition_values_from_llm_output(
        brain_definition.params, arguments
    )

    brain_search_params_values = extract_api_brain_definition_values_from_llm_output(
        brain_definition.search_params, arguments
    )

    secrets = brain_definition.secrets
    secrets_values = {}

    for secret in secrets:
        secret_value = brain_service.external_api_secrets_repository.read_secret(
            user_id=user_id, brain_id=brain_id, secret_name=secret.name
        )
        secrets_values[secret.name] = secret_value

    return get_api_call_response_as_text(
        api_url=brain_definition.url,
        params=brain_params_values,
        search_params=brain_search_params_values,
        secrets=secrets_values,
        method=brain_definition.method,
    )
