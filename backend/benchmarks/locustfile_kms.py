import io
import json
import os
import random
from typing import List
from uuid import UUID, uuid4

from locust import between, task
from locust.contrib.fasthttp import FastHttpUser
from pydantic import BaseModel
from quivr_api.modules.knowledge.dto.inputs import LinkKnowledgeBrain
from quivr_api.modules.knowledge.dto.outputs import KnowledgeDTO


class Data(BaseModel):
    brains_ids: List[UUID]
    knowledges_ids: List[UUID]
    vectors_ids: List[UUID]


load_params = {
    "data_path": "benchmarks/data.json",
    "file_size": 1024 * 1024,  # 1MB
    "parent_prob": 0.3,
    "folder_prob": 0.2,
    "km_root_prob": 0.2,
    "create_km_rate": 10,
    "list_km_rate": 10,
    "link_brain_rate": 5,
    "max_link_brains": 3,
    "delete_km_rate": 2,
}

with open(load_params["data_path"], "r") as f:
    data = Data.model_validate_json(f.read())

all_kms: List[KnowledgeDTO] = []
brains_ids = data.brains_ids


def is_folder() -> bool:
    return random.random() < load_params["folder_prob"]


def get_parent_id() -> str | None:
    if random.random() < load_params["parent_prob"] and len(all_kms) > 0:
        folders = list(filter(lambda k: k.is_folder, all_kms))
        if len(folders) == 0:
            return None
        folder = random.choice(folders)
        return str(folder.id)
    return None


class QuivrUser(FastHttpUser):
    wait_time = between(0.2, 1)  # Wait 1-5 seconds between tasks
    host = "http://localhost:5050"
    auth_headers = {
        "Authorization": "Bearer 123",
    }

    data = io.BytesIO(os.urandom(load_params["file_size"]))

    @task(load_params["create_km_rate"])
    def create_knowledge(self):
        km_data = {
            "file_name": "test_file.txt",
            "source": "local",
            "is_folder": is_folder(),
            "parent_id": get_parent_id(),
        }

        multipart_data = {
            "knowledge_data": (None, json.dumps(km_data), "application/json"),
            "file": ("test_file.txt", self.data, "application/octet-stream"),
        }
        response = self.client.post(
            "/knowledge/",
            headers=self.auth_headers,
            files=multipart_data,
        )
        returned_km = KnowledgeDTO.model_validate_json(response.text)
        all_kms.append(returned_km)

    create_knowledge.__name__ = "create_knowledge_1MB"

    @task(load_params["link_brain_rate"])
    def link_to_brains(self):
        if len(all_kms) == 0:
            return
        nb_brains = random.randint(1, load_params["max_link_brains"])
        random_brains = [random.choice(brains_ids) for _ in range(nb_brains)]
        random_km = random.choice(all_kms)
        json_data = LinkKnowledgeBrain(
            bulk_id=uuid4(), brain_ids=random_brains, knowledge=random_km
        ).model_dump_json()
        self.client.post(
            "/knowledge/link_to_brains/",
            data=json_data,
            headers={
                "Content-Type": "application/json",
                **self.auth_headers,
            },
        )

    link_to_brains.__name__ = "link_to_brain"

    @task(load_params["list_km_rate"])
    def list_knowledge_files(self):
        if random.random() < load_params["km_root_prob"] or len(all_kms) == 0:
            self.client.get(
                "/knowledge/files",
                headers=self.auth_headers,
                name="/knowledge/files",
            )
        else:
            random_km = random.choice(all_kms)
            self.client.get(
                f"/knowledge/files?parent_id={str(random_km.id)}",
                headers=self.auth_headers,
                name="/knowledge/files",
            )

    list_knowledge_files.__name__ = "list_knowledge_files"

    # @task(load_params["delete_km_rate"])
    # def delete_knowledge_files(self):
    #     only_files = [idx for idx, km in enumerate(all_kms) if not km.is_folder]
    #     if len(only_files) == 0:
    #         return
    #     random_index = random.choice(only_files)
    #     random_km = all_kms.pop(random_index)
    #     self.client.delete(
    #         f"/knowledge/{str(random_km.id)}",
    #         headers=self.auth_headers,
    #     )

    # delete_knowledge_files.__name__ = "delete_knowledge_file"
