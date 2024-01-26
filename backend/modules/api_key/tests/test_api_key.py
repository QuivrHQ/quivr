from modules.api_key.entity.api_key import ApiKey
from modules.api_key.service.api_key_service import ApiKeys

APIKeyService = ApiKeys()


def test_read_main(client, api_key):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_create_and_delete_api_key(client, api_key):
    # First, let's create an API key
    response = client.post(
        "/api-key",
        headers={
            "Authorization": "Bearer " + api_key,
        },
    )
    assert response.status_code == 200
    api_key_info = response.json()
    assert "api_key" in api_key_info

    # Extract the created api_key from the response
    api_key = api_key_info["api_key"]

    # Now, let's verify the API key
    verify_response = client.get(
        "/user",
        headers={
            "Authorization": f"Bearer {api_key}",
        },
    )
    assert verify_response.status_code == 200

    # Now, let's delete the API key
    assert "key_id" in api_key_info
    key_id = api_key_info["key_id"]

    delete_response = client.delete(
        f"/api-key/{key_id}", headers={"Authorization": f"Bearer {api_key}"}
    )
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "API key deleted."}


def test_api_key_model():
    api_key_data = {
        "api_key": "1234567890",
        "key_id": "abcd1234",
        "days": 7,
        "only_chat": False,
        "name": "Test API Key",
        "creation_time": "2022-01-01T00:00:00Z",
        "is_active": True,
    }
    api_key = ApiKey(**api_key_data)
    assert api_key.api_key == "1234567890"
    assert api_key.key_id == "abcd1234"
    assert api_key.days == 7
    assert api_key.only_chat is False
    assert api_key.name == "Test API Key"
    assert api_key.creation_time == "2022-01-01T00:00:00Z"
    assert api_key.is_active is True


def test_get_user_from_api_key(client, api_key):
    # Call the function with a test API key
    user = APIKeyService.get_user_id_by_api_key(api_key)

    # Use an assertion to check the returned user
    assert user is not None, "User should not be None"


def test_verify_api_key(client, api_key):
    # Call the function with a test API key
    user = APIKeyService.get_user_id_by_api_key(api_key).data[0]["user_id"]

    user_api_keys = APIKeyService.get_user_api_keys(user)
    # Use an assertion to check the returned user
    assert user_api_keys is not None, "User should not be None"
    assert len(user_api_keys) > 0, "User should have at least one API key"
