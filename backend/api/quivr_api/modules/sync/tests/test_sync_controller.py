from datetime import datetime
from io import BytesIO
from typing import Dict, List, Union
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from quivr_core.models import KnowledgeStatus
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.main import app
from quivr_api.middlewares.auth.auth_bearer import get_current_user
from quivr_api.modules.brain.entity.brain_entity import Brain, BrainType
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.knowledge.tests.conftest import FakeStorage
from quivr_api.modules.sync.controller.sync_routes import (
    get_knowledge_service,
    get_sync_service,
)
from quivr_api.modules.sync.dto.outputs import SyncProvider
from quivr_api.modules.sync.entity.sync_models import Sync, SyncFile
from quivr_api.modules.sync.repository.sync_repository import SyncsRepository
from quivr_api.modules.sync.service.sync_service import SyncsService
from quivr_api.modules.sync.utils.sync import BaseSync
from quivr_api.modules.user.entity.user_identity import User, UserIdentity

N_GET_FILES = 2

FOLDER_SYNC_FILE_IDS = [str(uuid4())[:8] for _ in range(N_GET_FILES)]


class BaseFakeSync(BaseSync):
    name = "FakeProvider"
    lower_name = "google"
    datetime_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"

    def get_files_by_id(self, credentials: Dict, file_ids: List[str]) -> List[SyncFile]:
        return [
            SyncFile(
                id=str(fid),
                name=f"file_{fid}",
                extension=".txt",
                web_view_link=f"test.com/{fid}",
                is_folder=False,
                last_modified_at=datetime.now(),
            )
            for fid in file_ids
        ]

    async def aget_files_by_id(
        self, credentials: Dict, file_ids: List[str]
    ) -> List[SyncFile]:
        return self.get_files_by_id(
            credentials=credentials,
            file_ids=file_ids,
        )

    def get_files(
        self, credentials: Dict, folder_id: str | None = None, recursive: bool = False
    ) -> List[SyncFile]:
        return [
            SyncFile(
                id=fid,
                name=f"file_{fid}",
                extension=".txt",
                web_view_link=f"test.com/{fid}",
                parent_id=folder_id,
                is_folder=idx % 2 == 0,
                last_modified_at=datetime.now(),
            )
            for idx, fid in enumerate(FOLDER_SYNC_FILE_IDS)
        ]

    async def aget_files(
        self, credentials: Dict, folder_id: str | None = None, recursive: bool = False
    ) -> List[SyncFile]:
        return self.get_files(
            credentials=credentials, folder_id=folder_id, recursive=recursive
        )

    def check_and_refresh_access_token(self, credentials: dict) -> Dict:
        raise NotImplementedError

    def download_file(
        self, credentials: Dict, file: SyncFile
    ) -> Dict[str, Union[str, BytesIO]]:
        raise NotImplementedError

    async def adownload_file(
        self, credentials: Dict, file: SyncFile
    ) -> Dict[str, Union[str, BytesIO]]:
        pass


@pytest_asyncio.fixture(scope="function")
async def user(session: AsyncSession) -> User:
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    assert user_1.id
    return user_1


@pytest_asyncio.fixture(scope="function")
async def sync(session: AsyncSession, user: User) -> User:
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
        name="test_brain",
        description="this is a test brain",
        brain_type=BrainType.integration,
    )
    session.add(brain_1)
    await session.commit()
    return brain_1


@pytest_asyncio.fixture(scope="function")
async def knowledge_sync(session, user: User, sync: Sync, brain: Brain):
    km = KnowledgeDB(
        file_name="sync_file_1.txt",
        extension=".txt",
        status=KnowledgeStatus.PROCESSED,
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1="test_sha1",
        brains=[brain],
        user_id=user.id,
        sync=sync,
        sync_file_id=FOLDER_SYNC_FILE_IDS[0],
    )
    session.add(km)
    await session.commit()
    await session.refresh(km)
    return km


@pytest_asyncio.fixture(scope="function")
async def test_client(session: AsyncSession, user: User):
    def default_current_user() -> UserIdentity:
        assert user.id
        return UserIdentity(email=user.email, id=user.id)

    async def _sync_service():
        fake_provider = {provider: BaseFakeSync() for provider in list(SyncProvider)}
        repository = SyncsRepository(session)
        repository.sync_provider_mapping = fake_provider
        return SyncsService(repository)

    async def _km_service():
        storage = FakeStorage()
        repository = KnowledgeRepository(session)
        return KnowledgeService(repository, storage)

    app.dependency_overrides[get_current_user] = default_current_user
    app.dependency_overrides[get_knowledge_service] = _km_service
    app.dependency_overrides[get_sync_service] = _sync_service

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides = {}


@pytest.mark.asyncio(loop_scope="session")
async def test_list_sync_no_knowledge(test_client: AsyncClient, sync: Sync):
    params = {"folder_id": 12}
    response = await test_client.get(f"/sync/{sync.id}/files", params=params)
    assert response.status_code == 200
    kms = response.json()
    assert len(kms) == N_GET_FILES


@pytest.mark.asyncio(loop_scope="session")
async def test_list_sync_with_knowledge(
    test_client: AsyncClient, sync: Sync, knowledge_sync
):
    params = {"folder_id": 12}
    response = await test_client.get(f"/sync/{sync.id}/files", params=params)
    assert response.status_code == 200
    kms = response.json()

    assert len(kms) == N_GET_FILES
    km = next(
        filter(lambda x: x["id"] == str(knowledge_sync.id), kms),
    )
    assert km, "at least one knowledge should "
    assert len(km["brains"]) == 1
