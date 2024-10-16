from io import BufferedReader, FileIO
from uuid import uuid4

import pytest_asyncio
from sqlmodel import select, text
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.modules.brain.entity.brain_entity import Brain, BrainType
from quivr_api.modules.knowledge.dto.outputs import KnowledgeDTO
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.modules.knowledge.repository.storage_interface import StorageInterface
from quivr_api.modules.sync.dto.outputs import SyncProvider
from quivr_api.modules.sync.entity.sync_models import Sync
from quivr_api.modules.user.entity.user_identity import User


class ErrorStorage(StorageInterface):
    async def upload_file_storage(
        self,
        knowledge: KnowledgeDB,
        knowledge_data: FileIO | BufferedReader | bytes,
        upsert: bool = False,
    ):
        raise SystemError

    def get_storage_path(
        self,
        knowledge: KnowledgeDB | KnowledgeDTO,
    ) -> str:
        if knowledge.id is None:
            raise ValueError("knowledge should have a valid id")
        return str(knowledge.id)

    async def remove_file(self, storage_path: str):
        raise SystemError

    async def download_file(self, knowledge: KnowledgeDB, **kwargs) -> bytes:
        raise NotImplementedError


class FakeStorage(StorageInterface):
    def __init__(self):
        self.storage = {}

    def get_storage_path(
        self,
        knowledge: KnowledgeDB | KnowledgeDTO,
    ) -> str:
        if knowledge.id is None:
            raise ValueError("knowledge should have a valid id")
        return str(knowledge.id)

    async def upload_file_storage(
        self,
        knowledge: KnowledgeDB,
        knowledge_data: FileIO | BufferedReader | bytes,
        upsert: bool = False,
    ):
        storage_path = f"{knowledge.id}"
        if not upsert and storage_path in self.storage:
            raise ValueError(f"File already exists at {storage_path}")
        if isinstance(knowledge_data, FileIO) or isinstance(
            knowledge_data, BufferedReader
        ):
            self.storage[storage_path] = knowledge_data.read()
        else:
            self.storage[storage_path] = knowledge_data

        return storage_path

    async def remove_file(self, storage_path: str):
        if storage_path not in self.storage:
            raise FileNotFoundError(f"File not found at {storage_path}")
        del self.storage[storage_path]

    # Additional helper methods for testing
    def get_file(self, storage_path: str) -> FileIO | BufferedReader | bytes:
        if storage_path not in self.storage:
            raise FileNotFoundError(f"File not found at {storage_path}")
        return self.storage[storage_path]

    def knowledge_exists(self, knowledge: KnowledgeDB | KnowledgeDTO) -> bool:
        return self.get_storage_path(knowledge) in self.storage

    def clear_storage(self):
        self.storage.clear()

    async def download_file(self, knowledge: KnowledgeDB, **kwargs) -> bytes:
        storage_path = self.get_storage_path(knowledge)
        return self.storage[storage_path]


@pytest_asyncio.fixture(scope="function")
async def other_user(session: AsyncSession):
    sql = text(
        """
        INSERT INTO "auth"."users" ("instance_id", "id", "aud", "role", "email", "encrypted_password", "email_confirmed_at", "invited_at", "confirmation_token", "confirmation_sent_at", "recovery_token", "recovery_sent_at", "email_change_token_new", "email_change", "email_change_sent_at", "last_sign_in_at", "raw_app_meta_data", "raw_user_meta_data", "is_super_admin", "created_at", "updated_at", "phone", "phone_confirmed_at", "phone_change", "phone_change_token", "phone_change_sent_at", "email_change_token_current", "email_change_confirm_status", "banned_until", "reauthentication_token", "reauthentication_sent_at", "is_sso_user", "deleted_at") VALUES
        ('00000000-0000-0000-0000-000000000000', :id , 'authenticated', 'authenticated', 'other@quivr.app', '$2a$10$vwKX0eMLlrOZvxQEA3Vl4e5V4/hOuxPjGYn9QK1yqeaZxa.42Uhze', '2024-01-22 22:27:00.166861+00', NULL, '', NULL, 'e91d41043ca2c83c3be5a6ee7a4abc8a4f4fb1afc0a8453c502af931', '2024-03-05 16:22:13.780421+00', '', '', NULL, '2024-03-30 23:21:12.077887+00', '{"provider": "email", "providers": ["email"]}', '{}', NULL, '2024-01-22 22:27:00.158026+00', '2024-04-01 17:40:15.332205+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL);
        """
    )
    await session.execute(sql, params={"id": uuid4()})

    other_user = (
        await session.exec(select(User).where(User.email == "other@quivr.app"))
    ).one()
    return other_user


@pytest_asyncio.fixture(scope="function")
async def user(session):
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    return user_1


@pytest_asyncio.fixture(scope="function")
async def sync(session: AsyncSession, user: User) -> Sync:
    assert user.id
    sync = Sync(
        name="test_sync",
        email="test@test.com",
        user_id=user.id,
        credentials={"test": "test"},
        provider=SyncProvider.GOOGLE,
    )

    session.add(sync)
    await session.commit()
    await session.refresh(sync)
    return sync


@pytest_asyncio.fixture(scope="function")
async def brain(session):
    brain_1 = Brain(
        name="brain_1",
        description="this is a test brain",
        brain_type=BrainType.integration,
    )
    session.add(brain_1)
    await session.commit()
    return brain_1


@pytest_asyncio.fixture(scope="function")
async def brain2(session):
    brain_1 = Brain(
        name="brain_2",
        description="this is a test brain",
        brain_type=BrainType.integration,
    )
    session.add(brain_1)
    await session.commit()
    return brain_1
