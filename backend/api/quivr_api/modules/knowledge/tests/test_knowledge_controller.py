import json

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.main import app
from quivr_api.middlewares.auth.auth_bearer import get_current_user
from quivr_api.modules.knowledge.controller.knowledge_routes import get_km_service
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
    def default_current_user() -> UserIdentity:
        assert user.id
        return UserIdentity(email=user.email, id=user.id)

    async def test_service():
        storage = FakeStorage()
        repository = KnowledgeRepository(session)
        return KnowledgeService(repository, storage)

    app.dependency_overrides[get_current_user] = default_current_user
    app.dependency_overrides[get_km_service] = test_service
    # app.dependency_overrides[get_async_session] = lambda: session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides = {}


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
