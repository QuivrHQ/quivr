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


def test_get_all_chats():
    # Making a GET request to the /chat endpoint to retrieve all chats
    response = client.get("/chat", headers={"Authorization": "Bearer " + API_KEY})

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    # Assert that the response data is a list
    response_data = response.json()

    # Optionally, you can loop through the chats and assert on specific fields
    for chat in response_data["chats"]:
        # e.g., assert that each chat object contains 'chat_id' and 'chat_name'
        assert "chat_id" in chat
        assert "chat_name" in chat


def test_create_chat_and_talk():
    # Make a POST request to chat with the default brain and a random chat name
    random_chat_name = "".join(
        random.choices(string.ascii_letters + string.digits, k=10)
    )

    brain_response = client.get(
        "/brains/default", headers={"Authorization": "Bearer " + API_KEY}
    )
    assert brain_response.status_code == 200
    default_brain_id = brain_response.json()["brain_id"]
    print("Default brain id: " + default_brain_id)

    # Create a chat
    response = client.post(
        "/chat",
        json={"name": random_chat_name},
        headers={"Authorization": "Bearer " + API_KEY},
    )
    assert response.status_code == 200

    # now talk to the chat with a question
    response_data = response.json()
    print(response_data)
    chat_id = response_data["chat_id"]
    response = client.post(
        f"/chat/{chat_id}/question?brain_id={default_brain_id}",
        json={
            "model": "gpt-3.5-turbo-0613",
            "question": "Hello, how are you?",
            "temperature": "0",
            "max_tokens": "256",
        },
        headers={"Authorization": "Bearer " + API_KEY},
    )
    assert response.status_code == 200

    response = client.post(
        f"/chat/{chat_id}/question?brain_id={default_brain_id}",
        json={
            "model": "gpt-4",
            "question": "Hello, how are you?",
            "temperature": "0",
            "max_tokens": "256",
        },
        headers={"Authorization": "Bearer " + API_KEY},
    )
    print(response)
    assert response.status_code == 200

    # Now, let's delete the chat
    # Assuming the chat_id is part of the chat_info response. If not, adjust this.
    delete_response = client.delete(
        "/chat/" + chat_id, headers={"Authorization": "Bearer " + API_KEY}
    )
    assert delete_response.status_code == 200


def test_explore_with_default_brain():
    # Retrieve the default brain
    brain_response = client.get(
        "/brains/default", headers={"Authorization": "Bearer " + API_KEY}
    )
    assert brain_response.status_code == 200
    default_brain_id = brain_response.json()["brain_id"]

    # Now use the default brain_id as parameter in the /explore/ endpoint
    response = client.get(
        f"/explore/{default_brain_id}",
        headers={"Authorization": "Bearer " + API_KEY},
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    # Optionally, you can assert on specific fields in the response data
    response_data = response.json()
    # e.g., assert that the response contains a 'results' field
    assert "documents" in response_data


def test_upload_and_delete_file():
    # Retrieve the default brain
    brain_response = client.get(
        "/brains/default", headers={"Authorization": "Bearer " + API_KEY}
    )
    assert brain_response.status_code == 200
    default_brain_id = brain_response.json()["brain_id"]

    # File to upload
    file_path = "test.txt"
    file_name = "test.txt"  # Assuming the name of the file on the server is the same as the local file name

    # Set enable_summarization flag
    enable_summarization = False

    # Upload the file
    with open(file_path, "rb") as file:
        upload_response = client.post(
            f"/upload?brain_id={default_brain_id}&enable_summarization={enable_summarization}",
            headers={"Authorization": "Bearer " + API_KEY},
            files={"uploadFile": file},
        )

    # Assert that the upload response status code is 200 (HTTP OK)
    assert upload_response.status_code == 200

    # Optionally, you can assert on specific fields in the upload response data
    upload_response_data = upload_response.json()
    assert "message" in upload_response_data

    # Delete the file
    delete_response = client.delete(
        f"/explore/{file_name}",
        headers={"Authorization": "Bearer " + API_KEY},
        params={"brain_id": default_brain_id},
    )

    # Assert that the delete response status code is 200 (HTTP OK)
    assert delete_response.status_code == 200

    # Optionally, you can assert on specific fields in the delete response data
    delete_response_data = delete_response.json()
    assert "message" in delete_response_data


def test_upload_explore_and_delete_file():
    # Retrieve the default brain
    brain_response = client.get(
        "/brains/default", headers={"Authorization": "Bearer " + API_KEY}
    )
    assert brain_response.status_code == 200
    default_brain_id = brain_response.json()["brain_id"]

    # File to upload
    file_path = "test.txt"
    file_name = "test.txt"  # Assuming the name of the file on the server is the same as the local file name

    # Set enable_summarization flag
    enable_summarization = False

    # Upload the file
    with open(file_path, "rb") as file:
        upload_response = client.post(
            f"/upload?brain_id={default_brain_id}&enable_summarization={enable_summarization}",
            headers={"Authorization": "Bearer " + API_KEY},
            files={"uploadFile": file},
        )

    # Assert that the upload response status code is 200 (HTTP OK)
    assert upload_response.status_code == 200

    # Optionally, you can assert on specific fields in the upload response data
    upload_response_data = upload_response.json()
    assert "message" in upload_response_data

    # Explore (Download) the file
    explore_response = client.get(
        f"/explore/{file_name}",
        headers={"Authorization": "Bearer " + API_KEY},
    )

    # Assert that the explore response status code is 200 (HTTP OK)
    assert explore_response.status_code == 200

    # Delete the file
    delete_response = client.delete(
        f"/explore/{file_name}",
        headers={"Authorization": "Bearer " + API_KEY},
        params={"brain_id": default_brain_id},
    )

    # Assert that the delete response status code is 200 (HTTP OK)
    assert delete_response.status_code == 200

    # Optionally, you can assert on specific fields in the delete response data
    delete_response_data = delete_response.json()
    assert "message" in delete_response_data


def test_get_user_info():
    # Send a request to get user information
    response = client.get("/user", headers={"Authorization": "Bearer " + API_KEY})

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    # Assert that the response contains the expected fields
    user_info = response.json()
    assert "email" in user_info
    assert "max_brain_size" in user_info
    assert "current_brain_size" in user_info
    assert "date" in user_info
