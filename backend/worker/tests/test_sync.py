import asyncio
import os
from typing import List, Tuple

import pytest
import pytest_asyncio
import sqlalchemy
from quivr_api.modules.brain.entity.brain_entity import Brain
from quivr_api.modules.chat.entity.chat import Chat, ChatHistory
from quivr_api.modules.sync.repository.sync_repository import NotionRepository
from quivr_api.modules.sync.service.sync_notion import (
    SyncNotionService,
    store_notion_pages,
)
from quivr_api.modules.user.entity.user_identity import User
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Session, create_engine, select
from sqlmodel.ext.asyncio.session import AsyncSession

pg_database_base_url = "postgres:postgres@localhost:54322/postgres"

TestData = Tuple[Brain, User, List[Chat], List[ChatHistory]]


@pytest.fixture(scope="session")
def event_loop(request: pytest.FixtureRequest):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def sync_engine():
    engine = create_engine(
        "postgresql://" + pg_database_base_url,
        echo=True if os.getenv("ORM_DEBUG") else False,
        pool_pre_ping=True,
        pool_size=10,
        pool_recycle=0.1,
    )

    yield engine


@pytest_asyncio.fixture()
async def sync_session(sync_engine):
    with sync_engine.connect() as conn:
        conn.begin()
        conn.begin_nested()
        sync_session = Session(conn, expire_on_commit=False)

        @sqlalchemy.event.listens_for(sync_session, "after_transaction_end")
        def end_savepoint(session, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                conn.sync_connection.begin_nested()

        yield sync_session


@pytest.fixture
def search_result():
    return [
        {
            "object": "page",
            "id": "77b34b29-96f5-487c-b594-ba69cbb951c0",
            "created_time": "2024-07-29T16:58:00.000Z",
            "last_edited_time": "2024-07-30T07:46:00.000Z",
            "created_by": {
                "object": "user",
                "id": "c8de6079-cc5a-4b46-8763-04f92b33fc18",
            },
            "last_edited_by": {
                "object": "user",
                "id": "c8de6079-cc5a-4b46-8763-04f92b33fc18",
            },
            "cover": None,
            "icon": {"type": "emoji", "emoji": ":brain:"},
            "parent": {
                "type": "page_id",
                "page_id": "6df769b6-3849-4141-b61c-14f0f6d4fa43",
            },
            "archived": False,
            "in_trash": False,
            "properties": {
                "title": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": "MEDDPICC", "link": None},
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default",
                            },
                            "plain_text": "MEDDPICC",
                            "href": None,
                        }
                    ],
                }
            },
            "url": "https://www.notion.so/MEDDPICC-77b34b2996f5487cb594ba69cbb951c0",
            "public_url": None,
        }
    ]


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


@pytest.fixture
def user_1(sync_session):
    user_1 = (
        sync_session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    return user_1


@pytest.mark.asyncio
async def test_store_notion_pages(session: AsyncSession, search_result, user_1):
    notion_repository = NotionRepository(session)
    notion_service = SyncNotionService(notion_repository)
    sync_files = await store_notion_pages(search_result, notion_service, user_1.id)
    assert sync_files
    assert len(sync_files) == 1
