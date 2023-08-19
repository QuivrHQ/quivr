def test_explore_with_default_brain(client, api_key):
    # Retrieve the default brain
    brain_response = client.get(
        "/brains/default", headers={"Authorization": "Bearer " + api_key}
    )
    assert brain_response.status_code == 200
    default_brain_id = brain_response.json()["id"]

    # Now use the default brain_id as parameter in the /explore/ endpoint
    response = client.get(
        f"/explore/{default_brain_id}",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Assert that the response status code is 200 (HTTP OK)
    assert response.status_code == 200

    # Optionally, you can assert on specific fields in the response data
    response_data = response.json()
    # e.g., assert that the response contains a 'results' field
    assert "documents" in response_data
