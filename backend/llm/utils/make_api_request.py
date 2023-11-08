import requests


def make_api_request(api_url, params, search_params, secrets) -> str:
    headers = {}

    api_url_with_search_params = api_url + "?"
    for search_param in search_params:
        api_url_with_search_params += f"{search_param}={search_params[search_param]}&"

    for secret in secrets:
        headers[secret] = secrets[secret]

    response = requests.get(
        url=api_url_with_search_params, params=params, headers=headers
    )

    return str(response.json())
