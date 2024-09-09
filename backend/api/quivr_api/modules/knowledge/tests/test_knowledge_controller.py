import json
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.main import app
from quivr_api.middlewares.auth.auth_bearer import get_current_user
from quivr_api.modules.dependencies import get_async_session
from quivr_api.modules.user.entity.user_identity import UserIdentity

client = TestClient(app)


def on_request(request):
    body = request.read()
    raw_request = (
        f"{request.method} {request.url} HTTP/1.1\n"
        + "\n".join(f"{k}: {v}" for k, v in request.headers.items())
        + "\n\n"
        + (body.decode("utf-8") if body else "")
    )
    print("Raw Request:\n", raw_request)


@pytest.fixture(scope="function")
def override_dependency(
    session: AsyncSession,
):
    def _current_user(*args, **kwargs) -> UserIdentity:
        return UserIdentity(
            email="admin@quivr.app",
            id=UUID("39418e3b-0258-4452-af60-7acfcc1263ff"),
        )

    async def test_session():
        return session

    app.dependency_overrides[get_current_user] = _current_user
    app.dependency_overrides[get_async_session] = test_session
    yield
    app.dependency_overrides = {}


def test_post_knowledge(override_dependency):
    km_data = {
        "file_name": "test_file.txt",
        "source": "local",
        "is_folder": False,
        "parent_id": None,
    }

    files = {
        "knowledge_data": (None, json.dumps(km_data), "application/json"),
        "file": ("test_file.txt", b"Test file content", "application/octet-stream"),
    }

    response = client.post(
        "/knowledge/",
        files=files,
    )

    assert response.status_code == 200


def test_add_knowledge_invalid_input(override_dependency):
    # Test with invalid input (missing both file_name and url)
    response = client.post("/knowledge/", json={})
    assert response.status_code == 400
    assert response.json()["detail"] == "Either file_name or url must be provided"
