def test_get_public_prompts(client, api_key):
    response = client.get(
        "/prompts",
        headers={"Authorization": "Bearer " + api_key},
    )
    assert response.status_code == 200
    assert len(response.json()) == 0
