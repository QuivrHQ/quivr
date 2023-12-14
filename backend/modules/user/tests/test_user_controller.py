def test_get_user_info(client, api_key):
    # Send a request to get user information
    response = client.get("/user", headers={"Authorization": "Bearer " + api_key})

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    # Assert that the response contains the expected fields
    user_info = response.json()
    print(user_info)
    assert "email" in user_info
    assert "max_brain_size" in user_info
    assert "current_brain_size" in user_info
    assert "date" in user_info
    assert "is_premium" in user_info
    assert "models" in user_info
    assert "requests_stats" in user_info
    assert "id" in user_info


def test_get_user_identity(client, api_key):
    # Send a request to get user identity
    response = client.get(
        "/user/identity", headers={"Authorization": "Bearer " + api_key}
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    # Assert that the response contains the expected fields
    user_identity = response.json()
    print(user_identity)
    assert "id" in user_identity
    assert "email" in user_identity
