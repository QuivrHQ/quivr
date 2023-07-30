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
