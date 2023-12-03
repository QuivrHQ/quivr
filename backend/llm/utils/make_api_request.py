import json

import requests
from logger import get_logger

logger = get_logger(__name__)


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
        response = requests.request(
            method,
            url=api_url_with_search_params,
            params=search_params or None,
            headers=headers or None,
            data=json.dumps(params) or None,
        )
        return response.text
    except Exception as e:
        logger.error(f"Error calling API: {e}")
        return str(e)
