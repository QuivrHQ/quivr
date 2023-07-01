import os

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

API_KEY = os.getenv("CI_TEST_API_KEY")


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_create_and_delete_api_key():
    # First, let's create an API key
    response = client.post(
        "/api-key",
        headers={
            "Authorization": "Bearer " + API_KEY,
        },
    )
    assert response.status_code == 200
    api_key_info = response.json()
    assert "api_key" in api_key_info

    # Extract the created api_key from the response
    api_key = api_key_info["api_key"]

    # Now, let's delete the API key
    # Assuming the key_id is part of the api_key_info response. If not, adjust this.
    key_id = api_key_info["key_id"]
    delete_response = client.delete(
        f"/api-key/{key_id}", headers={"Authorization": f"Bearer {API_KEY}"}
    )
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "API key deleted."}
