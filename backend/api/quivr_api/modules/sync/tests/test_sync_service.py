import pytest
import pytest_asyncio
from sqlmodel import select

from quivr_api.modules.sync.dto.outputs import SyncProvider
from quivr_api.modules.sync.entity.sync_models import Syncs
from quivr_api.modules.sync.repository.sync_repository import SyncsRepository
from quivr_api.modules.sync.service.sync_service import SyncsService
from quivr_api.modules.user.entity.user_identity import User


@pytest_asyncio.fixture(scope="function")
async def user(session):
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    return user_1


@pytest_asyncio.fixture(scope="function")
async def test_sync(session, user):
    assert user.id

    sync = Syncs(
        user_id=user.id,
        name="test_sync",
        provider=SyncProvider.GOOGLE,
    )

    session.add(sync)
    await session.commit()
    await session.refresh(sync)
    return sync


@pytest.mark.asyncio(loop_scope="session")
async def test_sync_delete_sync(session, test_sync):
    assert test_sync.id
    service = SyncsService(SyncsRepository(session))
    await service.delete_sync(test_sync.id, test_sync.user_id)
