import json
import os
import random
from typing import List
from uuid import UUID

from locust import between, task
from locust.contrib.fasthttp import FastHttpUser
from quivr_api.modules.brain.entity.brain_entity import Brain, BrainType
from quivr_api.modules.brain.entity.brain_user import BrainUserDB
from quivr_api.modules.dependencies import get_supabase_client
from quivr_api.modules.knowledge.dto.inputs import (
    KnowledgeUpdate,
    LinkKnowledgeBrain,
    UnlinkKnowledgeBrain,
)
from quivr_api.modules.knowledge.dto.outputs import KnowledgeDTO
from quivr_api.modules.user.entity.user_identity import User
from sqlmodel import Session, create_engine, select, text

pg_database_base_url = "postgresql://postgres:postgres@localhost:54322/postgres"


load_params = {
    "n_brains": 100,
    "file_size": 1024 * 1024,  # 1MB
    "parent_prob": 0.3,
    "folder_prob": 0.2,
    "km_root_prob": 0.2,
    # Task rates
    "create_km_rate": 10,
    "list_km_rate": 10,
    "link_brain_rate": 5,
    "max_link_brains": 3,
    "delete_km_rate": 2,
    "unlink_brain_rate": 5,
    "update_km_rate": 2,
}


all_kms: List[KnowledgeDTO] = []
brains_ids: List[UUID] = []


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


def setup_brains(session: Session, user_id: UUID) -> List[Brain]:
    brains = []
    brains_users = []

    for idx in range(load_params["n_brains"]):
        brain = Brain(
            name=f"brain_{idx}",
            description="this is a test brain",
            brain_type=BrainType.integration,
            status="private",
        )
        brains.append(brain)

    session.add_all(brains)
    session.commit()
    [session.refresh(b) for b in brains]

    for brain in brains:
        brain_user = BrainUserDB(
            brain_id=brain.brain_id,
            user_id=user_id,
            default_brain=True,
            rights="Owner",
        )
        brains_users.append(brain_user)
    session.add_all(brains_users)
    session.commit()

    return brains


class QuivrUser(FastHttpUser):
    # Wait 1-5 seconds between tasks
    wait_time = between(1, 5)
    host = "http://localhost:5050"
    auth_headers = {
        "Authorization": "Bearer 123",
    }

    data = os.urandom(load_params["file_size"])
    sync_engine = create_engine(
        pg_database_base_url,
        echo=False,
    )

    def on_start(self) -> None:
        global brains_ids

        with Session(self.sync_engine) as session:
            user = (
                session.exec(select(User).where(User.email == "admin@quivr.app"))
            ).one()
            assert user.id
            brains = setup_brains(session, user.id)
            brains_ids = [b.brain_id for b in brains]  # type: ignore

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

    @task(load_params["link_brain_rate"])
    def link_to_brains(self):
        global all_kms
        if len(all_kms) == 0:
            return
        nb_brains = random.randint(1, load_params["max_link_brains"])
        random_brains = [random.choice(brains_ids) for _ in range(nb_brains)]
        random_idx = random.choice(range(len(all_kms)))
        random_km = all_kms.pop(random_idx)
        json_data = LinkKnowledgeBrain(
            brain_ids=random_brains, knowledge=random_km
        ).model_dump_json()
        response = self.client.post(
            "/knowledge/link_to_brains/",
            data=json_data,
            headers={
                "Content-Type": "application/json",
                **self.auth_headers,
            },
        )
        response.raise_for_status()
        kms = [KnowledgeDTO.model_validate(r) for r in response.json()]
        all_kms.extend(kms)

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

    @task(load_params["unlink_brain_rate"])
    def unlink_knowledge_brain(self):
        global all_kms
        if len(all_kms) == 0:
            return
        random_idx = random.choice(range(len(all_kms)))
        random_km = all_kms.pop(random_idx)
        if len(random_km.brains) == 0:
            return
        random_brain = random.choice(random_km.brains)
        assert random_km.id
        json_data = UnlinkKnowledgeBrain(
            brain_ids=[UUID(random_brain["brain_id"])],
            knowledge_id=random_km.id,
        ).model_dump_json()
        self.client.delete(
            "/knowledge/unlink_from_brains/",
            data=json_data,
            headers={
                "Content-Type": "application/json",
                **self.auth_headers,
            },
        )

    @task(load_params["delete_km_rate"])
    def delete_knowledge_files(self):
        global all_kms
        only_files = [idx for idx, km in enumerate(all_kms) if not km.is_folder]
        if len(only_files) == 0:
            return
        random_index = random.choice(only_files)
        random_km = all_kms.pop(random_index)
        children_ids = [c.id for c in random_km.children]
        all_kms[:] = [k for k in all_kms if k.id not in children_ids]
        self.client.delete(
            f"/knowledge/{str(random_km.id)}",
            headers=self.auth_headers,
            name="/knowledge/delete",
        )

    @task(load_params["update_km_rate"])
    def update_knowledge(self):
        global all_kms
        if len(all_kms) == 0:
            return
        random_idx = random.choice(range(len(all_kms)))
        random_km = all_kms.pop(random_idx)
        assert random_km.id
        json_data = KnowledgeUpdate(file_name=f"file-{uuid4()}").model_dump_json(
            exclude_unset=True
        )
        response = self.client.patch(
            f"/knowledge/{random_km.id}/",
            data=json_data,
            name="/knowledge/update",
            headers={
                "Content-Type": "application/json",
                **self.auth_headers,
            },
        )
        assert response and response.text
        km = KnowledgeDTO.model_validate_json(response.text)
        all_kms.append(km)

    #  CRUD operations
    create_knowledge.__name__ = "create_knowledge_1MB"
    update_knowledge.__name__ = "update_knowledge"
    delete_knowledge_files.__name__ = "delete_knowledge_file"
    list_knowledge_files.__name__ = "list_knowledge_files"
    # Special linking/unlinking brains
    link_to_brains.__name__ = "link_to_brain"
    unlink_knowledge_brain.__name__ = "unlink_knowledge_brain"

    def on_stop(self):
        global brains_ids
        global all_kms
        all_kms = []
        brains_ids = []
        # Cleanup db
        with Session(self.sync_engine) as session:
            session.execute(text("DELETE FROM brains;"))
            session.execute(text("DELETE FROM knowledge;"))
            session.commit()
        # Cleanup storage
        client = get_supabase_client()
        client.storage.empty_bucket("quivr")
