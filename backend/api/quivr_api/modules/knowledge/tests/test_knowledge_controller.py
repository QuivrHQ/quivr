import json

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.main import app
from quivr_api.middlewares.auth.auth_bearer import get_current_user
from quivr_api.modules.dependencies import get_async_session
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.knowledge.tests.conftest import FakeStorage
from quivr_api.modules.user.entity.user_identity import User, UserIdentity


@pytest_asyncio.fixture(scope="function")
async def user(session: AsyncSession) -> User:
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    assert user_1.id
    return user_1


@pytest_asyncio.fixture(scope="function")
async def test_client(session: AsyncSession, user: User):
    assert user.id

    def default_current_user() -> UserIdentity:
        return UserIdentity(email=user.email, id=user.id)

    async def test_service():
        storage = FakeStorage()
        repository = KnowledgeRepository(session)
        return KnowledgeService(repository, storage)

    app.dependency_overrides[get_current_user] = default_current_user
    app.dependency_overrides[get_async_session] = lambda: session
    # app.dependency_overrides[get_service(KnowledgeService)] = test_service

    client = TestClient(app)
    yield client
    app.dependency_overrides = {}


@pytest.mark.skip
@pytest.mark.asyncio(loop_scope="session")
async def test_post_knowledge(test_client):
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

    response = test_client.post(
        "/knowledge/",
        files=multipart_data,
    )

    assert response.status_code == 200


@pytest.mark.skip
@pytest.mark.asyncio(loop_scope="session")
async def test_add_knowledge_invalid_input(test_client):
    response = test_client.post("/knowledge/", data={})
    assert response.status_code == 400
    assert response.json()["detail"] == "Either file_name or url must be provided"
