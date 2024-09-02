import asyncio
import os
from typing import Tuple

import pytest
import pytest_asyncio
import sqlalchemy
from quivr_api.modules.models.entity.model import Model
from quivr_api.modules.user.entity.user_identity import User
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

pg_database_base_url = "postgres:postgres@localhost:54322/postgres"

TestData = Tuple[Model, Model, User]


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(
        "postgresql+asyncpg://" + pg_database_base_url,
        echo=True if os.getenv("ORM_DEBUG") else False,
        future=True,
        pool_pre_ping=True,
        pool_size=10,
        pool_recycle=0.1,
    )
    yield engine


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
async def test_data(
    session: AsyncSession,
) -> TestData:
    # User data
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()

    model_1 = Model(
        name="this-is-a-fake-model", price=1, max_input=4000, max_output=2000
    )
    model_2 = Model(
        name="this-is-another-fake-model", price=5, max_input=8000, max_output=4000
    )

    session.add(model_1)
    session.add(model_2)

    await session.refresh(user_1)
    await session.commit()
    return model_1, model_2, user_1


@pytest_asyncio.fixture()
async def sample_models():
    return [
        Model(name="gpt-3.5-turbo", price=1, max_input=4000, max_output=2000),
        Model(name="gpt-4", price=5, max_input=8000, max_output=4000),
    ]
