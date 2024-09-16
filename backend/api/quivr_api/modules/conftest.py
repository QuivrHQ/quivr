import os

import pytest
import pytest_asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Session, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.modules.dependencies import get_supabase_client

pg_database_base_url = "postgres:postgres@localhost:54322/postgres"

sync_engine = create_engine(
    "postgresql://" + pg_database_base_url,
    echo=True if os.getenv("ORM_DEBUG") else False,
    pool_pre_ping=True,
    pool_size=10,
    pool_recycle=0.1,
)


async_engine = create_async_engine(
    "postgresql+asyncpg://" + pg_database_base_url,
    echo=True if os.getenv("ORM_DEBUG") else False,
    future=True,
)


@pytest.fixture(scope="function")
def sync_session():
    with sync_engine.connect() as conn:
        trans = conn.begin()
        nested = conn.begin_nested()
        sync_session = Session(
            conn,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

        @sqlalchemy.event.listens_for(sync_session, "after_transaction_end")
        def end_savepoint(session, transaction):
            nonlocal nested
            if not nested.is_active:
                nested = conn.begin_nested()

        yield sync_session
        trans.rollback()
        sync_session.close()


@pytest_asyncio.fixture(scope="function")
async def session():
    async with async_engine.connect() as conn:
        trans = await conn.begin()
        nested = await conn.begin_nested()
        async_session = AsyncSession(
            conn,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

        @sqlalchemy.event.listens_for(
            async_session.sync_session, "after_transaction_end"
        )
        def end_savepoint(session, transaction):
            nonlocal nested
            if not nested.is_active:
                nested = conn.sync_connection.begin_nested()

        yield async_session
        await trans.rollback()
        await async_session.close()


@pytest.fixture(scope="session")
def supabase_client():
    return get_supabase_client()
