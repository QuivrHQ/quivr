from uuid import UUID

from llm.utils.extract_brain_api_params_values_from_llm_output import (
    extract_brain_api_params_values_from_llm_output,
)
from llm.utils.make_api_request import make_api_request
from repository.api_brain_definition.get_api_brain_definition import (
    get_api_brain_definition,
)
from repository.external_api_secret.read_secret import read_secret


def call_brain_api(brain_id: UUID, user_id: UUID, arguments: dict):
    brain_definition = get_api_brain_definition(brain_id)
    if brain_definition is None:
        raise Exception("Brain definition not found")

    brain_params = brain_definition.params.properties
    brain_params_values = extract_brain_api_params_values_from_llm_output(
        brain_params, arguments
    )

    brain_search_params = brain_definition.search_params.properties
    brain_search_params_values = extract_brain_api_params_values_from_llm_output(
        brain_search_params, arguments
    )

    secrets = brain_definition.secrets
    secrets_values = {}

    for secret in secrets:
        secret_value = read_secret(
            user_id=user_id, brain_id=brain_id, secret_name=secret.name
        )
        secrets_values[secret.name] = secret_value

    return make_api_request(
        api_url=brain_definition.url,
        params=brain_params_values,
        search_params=brain_search_params_values,
        secrets=secrets_values,
    )
