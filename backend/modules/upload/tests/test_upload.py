import os
import json
import subprocess
# def test_upload_and_delete_file(client, api_key):
#     # Retrieve the default brain
#     brain_response = client.get(
#         "/brains/default", headers={"Authorization": "Bearer " + api_key}
#     )
#     assert brain_response.status_code == 200
#     default_brain_id = brain_response.json()["id"]

#     # File to upload
#     file_path = "test_files/test.txt"
#     file_name = "test.txt"  # Assuming the name of the file on the server is the same as the local file name

#     # Set enable_summarization flag
#     enable_summarization = False

#     # Upload the file
#     with open(file_path, "rb") as file:
#         upload_response = client.post(
#             f"/upload?brain_id={default_brain_id}&enable_summarization={enable_summarization}",
#             headers={"Authorization": "Bearer " + api_key},
#             files={"uploadFile": file},
#         )

#     # Assert that the upload response status code is 200 (HTTP OK)
#     assert upload_response.status_code == 200

#     # Optionally, you can assert on specific fields in the upload response data
#     upload_response_data = upload_response.json()
#     assert "message" in upload_response_data

#     # Delete the file
#     delete_response = client.delete(
#         f"/explore/{file_name}",
#         headers={"Authorization": "Bearer " + api_key},
#         params={"brain_id": default_brain_id},
#     )

#     # Assert that the delete response status code is 200 (HTTP OK)
#     assert delete_response.status_code == 200

#     # Optionally, you can assert on specific fields in the delete response data
#     delete_response_data = delete_response.json()
#     assert "message" in delete_response_data


# def test_upload_explore_and_delete_file_txt(client, api_key):
#     # Retrieve the default brain
#     brain_response = client.get(
#         "/brains/default", headers={"Authorization": "Bearer " + api_key}
#     )
#     assert brain_response.status_code == 200
#     default_brain_id = brain_response.json()["id"]

#     # File to upload
#     file_path = "test_files/test.txt"
#     file_name = "test.txt"  # Assuming the name of the file on the server is the same as the local file name

#     # Set enable_summarization flag
#     enable_summarization = False

#     # Upload the file
#     with open(file_path, "rb") as file:
#         upload_response = client.post(
#             f"/upload?brain_id={default_brain_id}&enable_summarization={enable_summarization}",
#             headers={"Authorization": "Bearer " + api_key},
#             files={"uploadFile": file},
#         )

#     # Assert that the upload response status code is 200 (HTTP OK)
#     assert upload_response.status_code == 200

#     # Optionally, you can assert on specific fields in the upload response data
#     upload_response_data = upload_response.json()
#     assert "message" in upload_response_data

#     # Explore (Download) the file
#     client.get(
#         f"/explore/{file_name}",
#         headers={"Authorization": "Bearer " + api_key},
#     )

#     # Delete the file
#     delete_response = client.delete(
#         f"/explore/{file_name}",
#         headers={"Authorization": "Bearer " + api_key},
#         params={"brain_id": default_brain_id},
#     )

#     # Assert that the delete response status code is 200 (HTTP OK)
#     assert delete_response.status_code == 200

#     # Optionally, you can assert on specific fields in the delete response data
#     delete_response_data = delete_response.json()
#     assert "message" in delete_response_data


# def test_upload_explore_and_delete_file_pdf(client, api_key):
#     # Retrieve the default brain
#     brain_response = client.get(
#         "/brains/default", headers={"Authorization": "Bearer " + api_key}
#     )
#     assert brain_response.status_code == 200
#     default_brain_id = brain_response.json()["id"]

#     # File to upload
#     file_path = "tests/test_files/test.pdf"
#     file_name = "test.pdf"  # Assuming the name of the file on the server is the same as the local file name

#     # Set enable_summarization flag
#     enable_summarization = False

#     # Upload the file
#     with open(file_path, "rb") as file:
#         upload_response = client.post(
#             f"/upload?brain_id={default_brain_id}&enable_summarization={enable_summarization}",
#             headers={"Authorization": "Bearer " + api_key},
#             files={"uploadFile": file},
#         )

#     # Assert that the upload response status code is 200 (HTTP OK)
#     assert upload_response.status_code == 200
#     # assert it starts with File uploaded successfully:

#     # Optionally, you can assert on specific fields in the upload response data
#     upload_response_data = upload_response.json()
#     assert "message" in upload_response_data
#     assert "type" in upload_response_data
#     assert upload_response_data["type"] == "success"

#     # Explore (Download) the file
#     explore_response = client.get(
#         f"/explore/{file_name}",
#         headers={"Authorization": "Bearer " + api_key},
#     )

#     # Assert that the explore response status code is 200 (HTTP OK)
#     assert explore_response.status_code == 200

#     # Delete the file
#     delete_response = client.delete(
#         f"/explore/{file_name}",
#         headers={"Authorization": "Bearer " + api_key},
#         params={"brain_id": default_brain_id},
#     )

#     # Assert that the delete response status code is 200 (HTTP OK)
#     assert delete_response.status_code == 200

#     # Optionally, you can assert on specific fields in the delete response data
#     delete_response_data = delete_response.json()
#     assert "message" in delete_response_data


# def test_upload_explore_and_delete_file_csv(client, api_key):
#     # Retrieve the default brain
#     brain_response = client.get(
#         "/brains/default", headers={"Authorization": "Bearer " + api_key}
#     )
#     assert brain_response.status_code == 200
#     default_brain_id = brain_response.json()["id"]

#     # File to upload
#     file_path = "tests/test_files/test.csv"
#     file_name = "test.csv"  # Assuming the name of the file on the server is the same as the local file name

#     # Set enable_summarization flag
#     enable_summarization = False

#     # Upload the file
#     with open(file_path, "rb") as file:
#         upload_response = client.post(
#             f"/upload?brain_id={default_brain_id}&enable_summarization={enable_summarization}",
#             headers={"Authorization": "Bearer " + api_key},
#             files={"uploadFile": file},
#         )

#     # Assert that the upload response status code is 200 (HTTP OK)
#     assert upload_response.status_code == 200

#     # Optionally, you can assert on specific fields in the upload response data
#     upload_response_data = upload_response.json()
#     assert "message" in upload_response_data

#     # Explore (Download) the file
#     client.get(
#         f"/explore/{file_name}",
#         headers={"Authorization": "Bearer " + api_key},
#     )

#     # Delete the file
#     delete_response = client.delete(
#         f"/explore/{file_name}",
#         headers={"Authorization": "Bearer " + api_key},
#         params={"brain_id": default_brain_id},
#     )

#     # Assert that the delete response status code is 200 (HTTP OK)
#     assert delete_response.status_code == 200

#     # Optionally, you can assert on specific fields in the delete response data
#     delete_response_data = delete_response.json()
#     assert "message" in delete_response_data


def test_upload_and_delete_file_bibtex(client, api_key):

    # Retrieve the default brain
    curl_command = [
        'curl', '-s',  # '-s' for silent mode to not show progress meter or error messages
        '-H', f"Authorization: Bearer {api_key}",
        '-H', "Accept: application/json",
        'http://localhost:5050/brains/default/'
    ]

    # Execute the curl command
    brain_response = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    response_json = json.loads(brain_response.stdout)
    default_brain_id = response_json["id"]

    # File to upload quivr/backend/modules/upload/tests/test_files/test.txt
    dir_path = os.path.dirname(os.path.realpath(__file__))

    # Construct the absolute path to the file
    file_path = os.path.join(dir_path, "test_files", "test.bib")
    file_name = "test.bib"  # Assuming the name of the file on the server is the same as the local file name

    # Set enable_summarization flag
    enable_summarization = False
    
    curl_command = [
    'curl', '-s', '-X', 'POST',
    '-H', f"Authorization: Bearer {api_key}",
    '-H', "Accept: application/json",
    '-F', f"uploadFile=@{file_path}",
    f'http://localhost:5050/upload?brain_id={default_brain_id}&enable_summarization={enable_summarization}'
    ]


    brain_response = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Optionally, you can assert on specific fields in the upload response data
    upload_response_data = brain_response
    assert "message" in json.loads(upload_response_data.stdout)

    # Delete the file
    curl_command = [
    'curl', '-s', '-X', 'POST',
    '-H', f"Authorization: Bearer {api_key}",
    '-H', "Accept: application/json",
    '-F', f"uploadFile=@{file_path}",
    f'http://localhost:5050/upload?brain_id={default_brain_id}&enable_summarization={enable_summarization}'
    ]

    brain_response = subprocess.run(curl_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Optionally, you can assert on specific fields in the upload response data
    upload_response_data = json.loads(brain_response.stdout)
    assert upload_response_data["detail"] == "File test.bib already exists in storage."