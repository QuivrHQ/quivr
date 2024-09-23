import json
from datetime import datetime
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
from quivr_api.modules.brain.entity.brain_user import BrainUserDB
from quivr_api.modules.knowledge.controller.knowledge_routes import (
    get_knowledge_service,
)
from quivr_api.modules.knowledge.dto.inputs import LinkKnowledgeBrain
from quivr_api.modules.knowledge.dto.outputs import KnowledgeDTO
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.knowledge.tests.conftest import FakeStorage
from quivr_api.modules.sync.dto.outputs import SyncProvider
from quivr_api.modules.sync.entity.sync_models import Sync
from quivr_api.modules.user.entity.user_identity import User, UserIdentity


@pytest_asyncio.fixture(scope="function")
async def user(session: AsyncSession) -> User:
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    assert user_1.id
    return user_1


@pytest_asyncio.fixture(scope="function")
async def brain(session, user):
    assert user.id
    brain_1 = Brain(
        name="test_brain",
        description="this is a test brain",
        brain_type=BrainType.integration,
    )
    session.add(brain_1)
    await session.commit()
    await session.refresh(brain_1)
    assert brain_1.brain_id
    brain_user = BrainUserDB(
        brain_id=brain_1.brain_id, user_id=user.id, default_brain=True, rights="Owner"
    )
    session.add(brain_user)
    await session.commit()
    return brain_1


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
async def test_client(session: AsyncSession, user: User):
    def default_current_user() -> UserIdentity:
        assert user.id
        return UserIdentity(email=user.email, id=user.id)

    async def test_service():
        storage = FakeStorage()
        repository = KnowledgeRepository(session)
        return KnowledgeService(repository, storage)

    app.dependency_overrides[get_current_user] = default_current_user
    app.dependency_overrides[get_knowledge_service] = test_service
    # app.dependency_overrides[get_async_session] = lambda: session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides = {}


@pytest.mark.asyncio(loop_scope="session")
async def test_post_knowledge_folder(test_client: AsyncClient):
    km_data = {
        "file_name": "test_file.txt",
        "source": "local",
        "is_folder": True,
        "parent_id": None,
    }

    multipart_data = {
        "knowledge_data": (None, json.dumps(km_data), "application/json"),
    }

    response = await test_client.post(
        "/knowledge/",
        files=multipart_data,
    )

    assert response.status_code == 200
    km = KnowledgeDTO.model_validate(response.json())

    assert km.id
    assert km.is_folder
    assert km.parent is None
    assert km.children == []


@pytest.mark.asyncio(loop_scope="session")
async def test_post_knowledge(test_client: AsyncClient):
    km_data = {
        "file_name": "test_file.txt",
        "source": "local",
        "is_folder": False,
        "parent_id": None,
    }

    multipart_data = {
        "knowledge_data": (None, json.dumps(km_data), "application/json"),
        "file": ("test_file.txt", b"Test file content", "application/octet-stream"),
    }

    response = await test_client.post(
        "/knowledge/",
        files=multipart_data,
    )

    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_add_knowledge_invalid_input(test_client):
    response = await test_client.post("/knowledge/", files={})
    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_link_knowledge_sync_file(
    monkeypatch,
    session: AsyncSession,
    test_client: AsyncClient,
    brain: Brain,
    user: User,
    sync: Sync,
):
    tasks = {}

    def _send_task(*args, **kwargs):
        tasks["args"] = args
        tasks["kwargs"] = {**kwargs["kwargs"]}

    monkeypatch.setattr("quivr_api.celery_config.celery.send_task", _send_task)

    assert user.id
    assert brain.brain_id
    km = KnowledgeDTO(
        id=None,
        file_name="test.txt",
        extension=".txt",
        status=None,
        user_id=user.id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        brains=[],
        source=SyncProvider.GOOGLE,
        source_link="drive://test.txt",
        sync_id=sync.id,
        sync_file_id="sync_file_id_1",
        parent=None,
        children=[],
    )
    json_data = LinkKnowledgeBrain(
        bulk_id=uuid4(), brain_ids=[brain.brain_id], knowledge=km
    ).model_dump_json()
    response = await test_client.post(
        "/knowledge/link_to_brains/",
        content=json_data,
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 201
    km = KnowledgeDTO.model_validate(response.json()[0])
    assert km.id
    assert km.status == KnowledgeStatus.PROCESSING
    assert len(km.brains) == 1

    # Assert task added to celery
    assert len(tasks) > 0
    assert tasks["args"] == ("process_file_task",)

    minimal_task_kwargs = {
        "knowledge_id": km.id,
    }
    all(
        minimal_task_kwargs[key] == tasks["kwargs"][key]  # type: ignore
        for key in minimal_task_kwargs
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_link_knowledge_folder(
    monkeypatch,
    session: AsyncSession,
    test_client: AsyncClient,
    brain: Brain,
    user: User,
    sync: Sync,
):
    assert brain.brain_id
    tasks = {}

    def _send_task(*args, **kwargs):
        tasks["args"] = args
        tasks["kwargs"] = {**kwargs["kwargs"]}

    monkeypatch.setattr("quivr_api.celery_config.celery.send_task", _send_task)

    folder_data = {
        "file_name": "folder",
        "source": "local",
        "is_folder": True,
        "parent_id": None,
    }
    response = await test_client.post(
        "/knowledge/",
        files={
            "knowledge_data": (None, json.dumps(folder_data), "application/json"),
        },
    )
    # 1. Insert folder
    folder_km = KnowledgeDTO.model_validate(response.json())
    file_data = {
        "file_name": "test_file.txt",
        "source": "local",
        "is_folder": True,
        "parent_id": str(folder_km.id),
    }

    multipart_data = {
        "knowledge_data": (None, json.dumps(file_data), "application/json"),
    }
    # 2. Insert file in folder
    response = await test_client.post(
        "/knowledge/",
        files=multipart_data,
    )
    file_km = KnowledgeDTO.model_validate(response.json())

    json_data = LinkKnowledgeBrain(
        bulk_id=uuid4(), brain_ids=[brain.brain_id], knowledge=folder_km
    ).model_dump_json()

    response = await test_client.post(
        "/knowledge/link_to_brains/",
        content=json_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 201
    updated_kms = [KnowledgeDTO.model_validate(d) for d in response.json()]

    # 3. Validate that created knowledges are correct
    assert len(updated_kms) == 2
    assert next(
        filter(lambda k: k.id == folder_km.id, updated_kms)
    ), "file not in updated list"
    assert next(
        filter(lambda k: k.id == file_km.id, updated_kms)
    ), "file not in updated list"
    for km in updated_kms:
        assert len(km.brains) == 1

    # 4. Assert both files are being scheduled for processing
    assert len(tasks) == 2
