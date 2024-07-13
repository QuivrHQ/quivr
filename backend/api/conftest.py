import asyncio
import os

import pytest
import pytest_asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

pg_database_base_url = "postgres:postgres@localhost:54322/postgres"


@pytest.fixture(scope="session")
def event_loop(request: pytest.FixtureRequest):
    loop = asyncio.get_event_loop_policy().new_event_loop()
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
