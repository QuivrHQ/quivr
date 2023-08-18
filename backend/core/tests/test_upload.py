def test_upload_and_delete_file(client, api_key):
    # Retrieve the default brain
    brain_response = client.get(
        "/brains/default", headers={"Authorization": "Bearer " + api_key}
    )
    assert brain_response.status_code == 200
    default_brain_id = brain_response.json()["id"]

    # File to upload
    file_path = "tests/test_files/test.txt"
    file_name = "test.txt"  # Assuming the name of the file on the server is the same as the local file name

    # Set enable_summarization flag
    enable_summarization = False

    # Upload the file
    with open(file_path, "rb") as file:
        upload_response = client.post(
            f"/upload?brain_id={default_brain_id}&enable_summarization={enable_summarization}",
            headers={"Authorization": "Bearer " + api_key},
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
        headers={"Authorization": "Bearer " + api_key},
        params={"brain_id": default_brain_id},
    )

    # Assert that the delete response status code is 200 (HTTP OK)
    assert delete_response.status_code == 200

    # Optionally, you can assert on specific fields in the delete response data
    delete_response_data = delete_response.json()
    assert "message" in delete_response_data


def test_upload_explore_and_delete_file_txt(client, api_key):
    # Retrieve the default brain
    brain_response = client.get(
        "/brains/default", headers={"Authorization": "Bearer " + api_key}
    )
    assert brain_response.status_code == 200
    default_brain_id = brain_response.json()["id"]

    # File to upload
    file_path = "tests/test_files/test.txt"
    file_name = "test.txt"  # Assuming the name of the file on the server is the same as the local file name

    # Set enable_summarization flag
    enable_summarization = False

    # Upload the file
    with open(file_path, "rb") as file:
        upload_response = client.post(
            f"/upload?brain_id={default_brain_id}&enable_summarization={enable_summarization}",
            headers={"Authorization": "Bearer " + api_key},
            files={"uploadFile": file},
        )

    # Assert that the upload response status code is 200 (HTTP OK)
    assert upload_response.status_code == 200

    # Optionally, you can assert on specific fields in the upload response data
    upload_response_data = upload_response.json()
    assert "message" in upload_response_data

    # Explore (Download) the file
    client.get(
        f"/explore/{file_name}",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Delete the file
    delete_response = client.delete(
        f"/explore/{file_name}",
        headers={"Authorization": "Bearer " + api_key},
        params={"brain_id": default_brain_id},
    )

    # Assert that the delete response status code is 200 (HTTP OK)
    assert delete_response.status_code == 200

    # Optionally, you can assert on specific fields in the delete response data
    delete_response_data = delete_response.json()
    assert "message" in delete_response_data


def test_upload_explore_and_delete_file_pdf(client, api_key):
    # Retrieve the default brain
    brain_response = client.get(
        "/brains/default", headers={"Authorization": "Bearer " + api_key}
    )
    assert brain_response.status_code == 200
    default_brain_id = brain_response.json()["id"]

    # File to upload
    file_path = "tests/test_files/test.pdf"
    file_name = "test.pdf"  # Assuming the name of the file on the server is the same as the local file name

    # Set enable_summarization flag
    enable_summarization = False

    # Upload the file
    with open(file_path, "rb") as file:
        upload_response = client.post(
            f"/upload?brain_id={default_brain_id}&enable_summarization={enable_summarization}",
            headers={"Authorization": "Bearer " + api_key},
            files={"uploadFile": file},
        )

    # Assert that the upload response status code is 200 (HTTP OK)
    assert upload_response.status_code == 200
    # assert it starts with File uploaded successfully:

    # Optionally, you can assert on specific fields in the upload response data
    upload_response_data = upload_response.json()
    assert "message" in upload_response_data
    assert "type" in upload_response_data
    assert upload_response_data["type"] == "success"

    # Explore (Download) the file
    explore_response = client.get(
        f"/explore/{file_name}",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Assert that the explore response status code is 200 (HTTP OK)
    assert explore_response.status_code == 200

    # Delete the file
    delete_response = client.delete(
        f"/explore/{file_name}",
        headers={"Authorization": "Bearer " + api_key},
        params={"brain_id": default_brain_id},
    )

    # Assert that the delete response status code is 200 (HTTP OK)
    assert delete_response.status_code == 200

    # Optionally, you can assert on specific fields in the delete response data
    delete_response_data = delete_response.json()
    assert "message" in delete_response_data


def test_upload_explore_and_delete_file_csv(client, api_key):
    # Retrieve the default brain
    brain_response = client.get(
        "/brains/default", headers={"Authorization": "Bearer " + api_key}
    )
    assert brain_response.status_code == 200
    default_brain_id = brain_response.json()["id"]

    # File to upload
    file_path = "tests/test_files/test.csv"
    file_name = "test.csv"  # Assuming the name of the file on the server is the same as the local file name

    # Set enable_summarization flag
    enable_summarization = False

    # Upload the file
    with open(file_path, "rb") as file:
        upload_response = client.post(
            f"/upload?brain_id={default_brain_id}&enable_summarization={enable_summarization}",
            headers={"Authorization": "Bearer " + api_key},
            files={"uploadFile": file},
        )

    # Assert that the upload response status code is 200 (HTTP OK)
    assert upload_response.status_code == 200

    # Optionally, you can assert on specific fields in the upload response data
    upload_response_data = upload_response.json()
    assert "message" in upload_response_data

    # Explore (Download) the file
    client.get(
        f"/explore/{file_name}",
        headers={"Authorization": "Bearer " + api_key},
    )

    # Delete the file
    delete_response = client.delete(
        f"/explore/{file_name}",
        headers={"Authorization": "Bearer " + api_key},
        params={"brain_id": default_brain_id},
    )

    # Assert that the delete response status code is 200 (HTTP OK)
    assert delete_response.status_code == 200

    # Optionally, you can assert on specific fields in the delete response data
    delete_response_data = delete_response.json()
    assert "message" in delete_response_data
