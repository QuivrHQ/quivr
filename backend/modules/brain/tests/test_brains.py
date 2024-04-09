import random
import string

from modules.brain.service.brain_user_service import BrainUserService

brain_user_service = BrainUserService()

def test_create_brain(client, api_key):
    # Generate a random name for the brain
    random_brain_name = "".join(
        random.choices(string.ascii_letters + string.digits, k=10)
    )

    # Set up the request payload
    payload = {
        "name": random_brain_name,
        "status": "public",
        "model": "gpt-3.5-turbo-0125",
        "temperature": 0,
        "max_tokens": 2000,
        "brain_type": "doc",
    }

    # Making a POST request to the /brains/ endpoint
    response = client.post(
        "/brains/",
        json=payload,
        headers={"Authorization": "Bearer " + api_key},
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


def test_retrieve_all_brains(client, api_key):
    # Making a GET request to the /brains/ endpoint to retrieve all brains for the current user
    response = client.get(
        "/brains/",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    response_data = response.json()
    # Optionally, you can loop through the brains and assert on specific fields in each brain
    for brain in response_data["brains"]:
        assert "id" in brain
        assert "name" in brain


def test_retrieve_one_brain(client, api_key):
    # Making a GET request to the /brains/default/ endpoint
    response = client.get(
        "/brains/default/",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    response_data = response.json()

    # Extract the brain_id from the response
    brain_id = response_data["id"]

    # Making a GET request to the /brains/{brain_id}/ endpoint
    response = client.get(
        f"/brains/{brain_id}/",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    brain = response.json()
    assert "id" in brain
    assert "name" in brain


def test_delete_all_brains(client, api_key):
    # First, retrieve all brains for the current user
    response = client.get(
        "/brains/",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    response_data = response.json()

    # Loop through each brain and send a DELETE request
    for brain in response_data["brains"]:
        brain_id = brain["id"]

        # Send a DELETE request to delete the specific brain
        delete_response = client.delete(
            f"/brains/{brain_id}/subscription",
            headers={"Authorization": "Bearer " + api_key},
        )

        # Assert that the DELETE response status code is 200 (HTTP OK)
        assert delete_response.status_code == 200

    # Finally, retrieve all brains for the current user
    response = client.get(
        "/brains/",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data["brains"]) == 0


def test_delete_all_brains_and_get_default_brain(client, api_key):
    # First create a new brain
    test_create_brain(client, api_key)

    # Now, retrieve all brains for the current user
    response = client.get(
        "/brains/",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200
    assert len(response.json()["brains"]) > 0

    test_delete_all_brains(client, api_key)

    # Get the default brain, it should create one if it doesn't exist
    response = client.get(
        "/brains/default/",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200
    assert response.json()["name"] == "Default brain"


def test_set_as_default_brain_endpoint(client, api_key):
    random_brain_name = "".join(
        random.choices(string.ascii_letters + string.digits, k=10)
    )
    # Set up the request payload
    payload = {
        "name": random_brain_name,
        "status": "public",
        "model": "gpt-3.5-turbo-0125",
        "temperature": 0,
        "max_tokens": 256,
    }

    # Making a POST request to the /brains/ endpoint
    response = client.post(
        "/brains/",
        json=payload,
        headers={"Authorization": "Bearer " + api_key},
    )

    response_data = response.json()

    brain_id = response_data["id"]

    # Make a POST request to set the brain as default for the user
    response = client.post(
        f"/brains/{brain_id}/default",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    # Assert the response message
    assert response.json() == {
        "message": f"Brain {brain_id} has been set as default brain."
    }

    # Check if the brain is now the default for the user

    # Send a request to get user information
    response = client.get("/user", headers={"Authorization": "Bearer " + api_key})
    # Assert that the response contains the expected fields
    user_info = response.json()
    user_id = user_info["id"]

    default_brain = brain_user_service.get_user_default_brain(user_id)
    assert default_brain is not None
    assert str(default_brain.brain_id) == str(brain_id)


def create_public_brain_retrieve_and_then_delete(client, api_key):
    # Generate a random name for the brain
    random_brain_name = "".join(
        random.choices(string.ascii_letters + string.digits, k=10)
    )

    # Set up the request payload
    payload = {
        "name": random_brain_name,
        "status": "public",
        "model": "gpt-3.5-turbo-0125",
        "temperature": 0,
        "max_tokens": 256,
        "brain_type": "doc",
    }

    # Making a POST request to the /brains/ endpoint
    response = client.post(
        "/brains/",
        json=payload,
        headers={"Authorization": "Bearer " + api_key},
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

    # Now, retrieve all brains for the current user
    response = client.get(
        "/brains/public",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200
    assert len(response.json()["brains"]) > 0

    # Check brain is in public list
    brain_id = response_data["id"]
    public_brains = response.json()["brains"]
    assert brain_id in [brain["id"] for brain in public_brains]

    # Delete the brain
    response = client.delete(
        f"/brains/{brain_id}/subscription",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Assert that the DELETE response status code is 200 (HTTP OK)
    assert response.status_code == 200
