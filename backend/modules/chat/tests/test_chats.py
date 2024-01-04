import random
import string


def test_get_all_chats(client, api_key):
    # Making a GET request to the /chat endpoint to retrieve all chats
    response = client.get(
        "/chat",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    # Assert that the response data is a list
    response_data = response.json()

    # Optionally, you can loop through the chats and assert on specific fields
    for chat in response_data["chats"]:
        # e.g., assert that each chat object contains 'chat_id' and 'chat_name'
        assert "chat_id" in chat
        assert "chat_name" in chat


def test_create_chat_and_talk(client, api_key):
    # Make a POST request to chat with the default brain and a random chat name
    random_chat_name = "".join(
        random.choices(string.ascii_letters + string.digits, k=10)
    )

    brain_response = client.get(
        "/brains/default", headers={"Authorization": "Bearer " + api_key}
    )
    assert brain_response.status_code == 200
    default_brain_id = brain_response.json()["id"]
    print("Default brain id: " + default_brain_id)

    # Create a chat
    response = client.post(
        "/chat",
        json={"name": random_chat_name},
        headers={"Authorization": "Bearer " + api_key},
    )
    assert response.status_code == 200

    # now talk to the chat with a question
    response_data = response.json()
    print(response_data)
    chat_id = response_data["chat_id"]
    response = client.post(
        f"/chat/{chat_id}/question?brain_id={default_brain_id}",
        json={
            "model": "gpt-3.5-turbo-1106",
            "question": "Hello, how are you?",
            "temperature": "0",
            "max_tokens": "256",
        },
        headers={"Authorization": "Bearer " + api_key},
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
        headers={"Authorization": "Bearer " + api_key},
    )
    print(response)
    assert response.status_code == 200

    # Now, let's delete the chat
    delete_response = client.delete(
        "/chat/" + chat_id, headers={"Authorization": "Bearer " + api_key}
    )
    assert delete_response.status_code == 200


def test_create_chat_and_talk_with_no_brain(client, api_key):
    # Make a POST request to chat with no brain id and a random chat name
    random_chat_name = "".join(
        random.choices(string.ascii_letters + string.digits, k=10)
    )

    # Create a chat
    response = client.post(
        "/chat",
        json={"name": random_chat_name},
        headers={"Authorization": "Bearer " + api_key},
    )
    assert response.status_code == 200

    # now talk to the chat with a question
    response_data = response.json()
    print(response_data)
    chat_id = response_data["chat_id"]
    response = client.post(
        f"/chat/{chat_id}/question?brain_id=",
        json={
            "model": "gpt-3.5-turbo-1106",
            "question": "Hello, how are you?",
            "temperature": "0",
            "max_tokens": "256",
        },
        headers={"Authorization": "Bearer " + api_key},
    )
    assert response.status_code == 200

    # Now, let's delete the chat
    delete_response = client.delete(
        "/chat/" + chat_id, headers={"Authorization": "Bearer " + api_key}
    )
    assert delete_response.status_code == 200


# Test delete all chats for a user
def test_delete_all_chats(client, api_key):
    chats = client.get("/chat", headers={"Authorization": "Bearer " + api_key})
    assert chats.status_code == 200
    chats_data = chats.json()
    for chat in chats_data["chats"]:
        # e.g., assert that each chat object contains 'chat_id' and 'chat_name'
        assert "chat_id" in chat
        assert "chat_name" in chat
        chat_id = chat["chat_id"]
        delete_response = client.delete(
            "/chat/" + chat_id, headers={"Authorization": "Bearer " + api_key}
        )
        assert delete_response.status_code == 200
