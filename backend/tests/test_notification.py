def test_get_notifications(client, api_key):
    # Send a request to get notifications
    response = client.get(
        "/notifications/ab780686-bcf3-46cb-9068-d724628caccd",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    # Assert that the response contains the expected fields
    notifications = response.json()
    assert notifications == []
