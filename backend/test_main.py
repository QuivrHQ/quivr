import os
import random
import string
import uuid

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

    # Now, let's verify the API key
    verify_response = client.get(
        "/user",
        headers={
            "Authorization": f"Bearer {api_key}",
        },
    )
    assert verify_response.status_code == 200

    # Now, let's delete the API key
    # Assuming the key_id is part of the api_key_info response. If not, adjust this.
    key_id = api_key_info["key_id"]
    delete_response = client.delete(
        f"/api-key/{key_id}", headers={"Authorization": f"Bearer {API_KEY}"}
    )
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "API key deleted."}


def test_retrieve_default_brain():
    # Making a GET request to the /brains/default/ endpoint
    response = client.get(
        "/brains/default/", headers={"Authorization": "Bearer " + API_KEY}
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    # Optionally, assert on specific fields in the response
    response_data = response.json()
    # e.g., assert that the response contains a 'brain_id' field
    assert "brain_id" in response_data


def test_create_brain():
    # Generate a random UUID for brain_id
    random_brain_id = str(uuid.uuid4())
    random_brain_id = str(uuid.uuid4())

    # Generate a random name for the brain
    random_brain_name = "".join(
        random.choices(string.ascii_letters + string.digits, k=10)
    )

    # Set up the request payload
    payload = {
        "brain_id": random_brain_id,
        "name": random_brain_name,
        "status": "public",
        "model": "gpt-3.5-turbo-0613",
        "temperature": 0,
        "max_tokens": 256,
        "file_sha1": "",
    }

    # Making a POST request to the /brains/ endpoint
    response = client.post(
        "/brains/", json=payload, headers={"Authorization": "Bearer " + API_KEY}
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    # Optionally, assert on specific fields in the response
    response_data = response.json()
    # e.g., assert that the response contains a 'brain_id' field
    assert "id" in response_data
    assert "name" in response_data

    # Optionally, assert that the returned 'name' matches the one sent in the request
    assert response_data["name"] == payload["name"]


def test_retrieve_all_brains():
    # Making a GET request to the /brains/ endpoint to retrieve all brains for the current user
    response = client.get("/brains/", headers={"Authorization": "Bearer " + API_KEY})

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    response_data = response.json()
    # Optionally, you can loop through the brains and assert on specific fields in each brain
    for brain in response_data["brains"]:
        assert "id" in brain
        assert "name" in brain


def test_delete_all_brains():
    # First, retrieve all brains for the current user
    response = client.get("/brains/", headers={"Authorization": "Bearer " + API_KEY})

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    response_data = response.json()

    # Loop through each brain and send a DELETE request
    for brain in response_data["brains"]:
        brain_id = brain["id"]

        # Send a DELETE request to delete the specific brain
        delete_response = client.delete(
            f"/brains/{brain_id}/", headers={"Authorization": "Bearer " + API_KEY}
        )

        # Assert that the DELETE response status code is 200 (HTTP OK)
        assert delete_response.status_code == 200
