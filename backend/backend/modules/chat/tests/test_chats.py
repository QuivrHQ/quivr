import asyncio
from uuid import uuid4

import pytest
import pytest_asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel, create_engine, select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.modules.chat.entity.chat import Chat
from backend.modules.chat.repository.chats import ChatRepository
from backend.modules.user.entity.user_identity import User

pg_database_url = "postgres:postgres@localhost:54322/postgres"


@pytest.fixture(scope="session", autouse=True)
def db_setup():
    # setup
    sync_engine = create_engine("postgresql://" + pg_database_url, echo=True)
    #  TODO(@amine) : for now don't drop anything
    SQLModel.metadata.create_all(sync_engine, checkfirst=True)
    yield sync_engine
    # teardown
    # NOTE: For now we rely on Supabase migrations for defining schemas
    # SQLModel.metadata.drop_all(sync_engine)


@pytest_asyncio.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(
        "postgresql+asyncpg://" + pg_database_url,
        echo=True,  # future=True
    )
    yield engine


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def session(async_engine):
    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()
        async_session = AsyncSession(conn, expire_on_commit=False)

        @sqlalchemy.event.listens_for(
            async_session.sync_session, "after_transaction_end"
        )
        def end_savepoint(session, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                conn.sync_connection.begin_nested()

        yield async_session


@pytest_asyncio.fixture()
async def local_user(session: AsyncSession) -> User:
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    chat_1 = Chat(chat_name="chat1", user=user_1)
    chat_2 = Chat(chat_name="chat2", user=user_1)
    session.add(chat_1)
    session.add(chat_2)
    # await session.refresh(user_1)
    await session.commit()
    return user_1


@pytest.mark.asyncio
async def test_get_user_chats_empty(session):
    repo = ChatRepository(session)
    chats = await repo.get_user_chats(user_id=uuid4())
    assert len(chats) == 0


@pytest.mark.asyncio
async def test_get_user_chats(session: AsyncSession, local_user: User):
    repo = ChatRepository(session)
    assert local_user.id is not None
    chats = await repo.get_user_chats(local_user.id)
    assert len(chats) == 2
