from uuid import UUID
import requests
from logger import get_logger
logger = get_logger(__name__)

from fastapi import HTTPException

from modules.brain.entity.api_brain_definition_entity import ApiBrainDefinitionSchema
from modules.brain.service.api_brain_definition_service import ApiBrainDefinitionService
from modules.brain.service.brain_service import BrainService

brain_service = BrainService()
api_brain_definition_service = ApiBrainDefinitionService()


def get_api_call_response_as_text(
    method, api_url, params, search_params, secrets
) -> str:
    headers = {}

    api_url_with_search_params = api_url
    if search_params:
        api_url_with_search_params += "?"
        for search_param in search_params:
            api_url_with_search_params += (
                f"{search_param}={search_params[search_param]}&"
            )

    for secret in secrets:
        headers[secret] = secrets[secret]

    try:
        if method in ["GET", "DELETE"]:
            response = requests.request(
                method,
                url=api_url_with_search_params,
                params=params or None,
                headers=headers or None,
            )
        elif method in ["POST", "PUT", "PATCH"]:
            response = requests.request(
                method,
                url=api_url_with_search_params,
                json=params or None,
                headers=headers or None,
            )
        else:
            raise ValueError(f"Invalid method: {method}")

        return response.text

    except Exception as e:
        logger.error(f"Error calling API: {e}")
        return None


def extract_api_brain_definition_values_from_llm_output(
    brain_schema: ApiBrainDefinitionSchema, arguments: dict
) -> dict:
    params_values = {}
    properties = brain_schema.properties
    required_values = brain_schema.required
    for property in properties:
        if property.name in arguments:
            if property.type == "number":
                params_values[property.name] = float(arguments[property.name])
            else:
                params_values[property.name] = arguments[property.name]
            continue

        if property.name in required_values:
            raise HTTPException(
                status_code=400,
                detail=f"Required parameter {property.name} not found in arguments",
            )

    return params_values


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
