import os
import random
import tempfile
from typing import List
from uuid import UUID

from locust import between, task
from locust.contrib.fasthttp import FastHttpUser
from pydantic import BaseModel

FILE_SIZE = 1024 * 1024


class Data(BaseModel):
    brains_ids: List[UUID]
    knowledges_ids: List[UUID]
    vectors_ids: List[UUID]


with open("data.json", "r") as f:
    data = Data.model_validate_json(f.read())


class QuivrUser(FastHttpUser):
    wait_time = between(0.2, 1)  # Wait 1-5 seconds between tasks
    host = "http://localhost:5050"
    auth_headers = {
        "Authorization": "Bearer 123",
    }
    query_params = "?brain_id=40ba47d7-51b2-4b2a-9247-89e29619efb0"

    def on_start(self):
        # Prepare the file to be uploaded
        self.file_path = "test_file.txt"
        with open(self.file_path, "wb") as f:
            f.write(os.urandom(1024))  # 1 KB

    @task(10)
    def upload_file(self):
        with tempfile.NamedTemporaryFile(suffix="_file.txt") as fp:
            fp.write(os.urandom(1024))  # 1 KB
            fp.flush()
            files = {
                "uploadFile": fp,
            }
            response = self.client.post(
                f"/upload{self.query_params}",
                files=files,
                headers={"Content-Type": "multipart/form-data", **self.auth_headers},
            )

            # Check if the upload was successful
            if response.status_code == 200:
                print(f"File uploaded successfully. Response: {response.text}")
            else:
                print(f"File upload failed. Status code: {response.status_code}")

    upload_file.__name__ = f"{upload_file.__name__}_1MB"

    @task(10)
    def get_brains(self):
        self.client.get("/brains", headers=self.auth_headers)

    @task(10)
    def get_brain_by_id(self):
        random_brain_id = random.choice(data.brains_ids)
        self.client.get(f"/brains/{random_brain_id}", headers=self.auth_headers)

    @task(10)
    def get_knowledge_by_id(self):
        random_brain_id = random.choice(data.brains_ids)
        self.client.get(
            f"/knowledge?brain_id={random_brain_id}", headers=self.auth_headers
        )

    @task(2)
    def get_knowledge_signed_url(self):
        random_knowledge = random.choice(data.knowledges_ids)
        self.client.get(
            f"/knowledge/{random_knowledge}/signed_download_url",
            headers=self.auth_headers,
        )

    @task(1)
    def delete_knowledge(self):
        random_knowledge = random.choice(data.knowledges_ids)
        data.knowledges_ids.remove(random_knowledge)
        self.client.delete(
            f"/knowledge/{random_knowledge}",
            headers=self.auth_headers,
        )

    def on_stop(self):
        # Clean up the test file
        if os.path.exists(self.file_path):
            os.remove(self.file_path)


# GET Knowledge brain
# DELETE knowledge cascades on vectors
# GET /knowledge/{knowledge_id}/signed_download_url
