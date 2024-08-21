import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest
import pytest_asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Session, create_engine, select
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.modules.sync.entity.notion_page import (
    BlockParent,
    DatabaseParent,
    NotionPage,
    NotionSearchResult,
    PageParent,
    PageProps,
    TextContent,
    Title,
    TitleItem,
    WorkspaceParent,
)
from quivr_api.modules.user.entity.user_identity import User

pg_database_base_url = "postgres:postgres@localhost:54322/postgres"


@pytest.fixture(scope="function")
def page_response() -> dict[str, Any]:
    json_path = (
        Path(os.getenv("PYTEST_CURRENT_TEST").split(":")[0])
        .parent.absolute()
        .joinpath("page.json")
    )
    with open(json_path, "r") as f:
        page = json.load(f)
    return page


@pytest.fixture(scope="function")
def fetch_response():
    return [
        {
            "object": "page",
            "id": "27b26c5a-e86f-470a-a5fc-27a3fc308850",
            "created_time": "2024-05-02T09:03:00.000Z",
            "last_edited_time": "2024-08-19T10:01:00.000Z",
            "created_by": {
                "object": "user",
                "id": "e2f8bfda-3b98-466e-a2c1-39e5f0f64881",
            },
            "last_edited_by": {
                "object": "user",
                "id": "f87bcc4b-68ee-4d44-b518-3d2d19ffedc2",
            },
            "cover": None,
            "icon": {"type": "emoji", "emoji": "🌇"},
            "parent": {"type": "workspace", "workspace": True},
            "archived": False,
            "in_trash": False,
            "properties": {
                "title": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": "Investors", "link": None},
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default",
                            },
                            "plain_text": "Investors",
                            "href": None,
                        }
                    ],
                }
            },
            "url": "https://www.notion.so/Investors-27b26c5ae86f470aa5fc27a3fc308850",
            "public_url": None,
        },
        {
            "object": "page",
            "id": "ff799030-eae6-4c81-8631-ee2653f27af8",
            "created_time": "2024-04-04T23:24:00.000Z",
            "last_edited_time": "2024-08-19T10:01:00.000Z",
            "created_by": {
                "object": "user",
                "id": "c8de6079-cc5a-4b46-8763-04f92b33fc18",
            },
            "last_edited_by": {
                "object": "user",
                "id": "f87bcc4b-68ee-4d44-b518-3d2d19ffedc2",
            },
            "cover": None,
            "icon": {"type": "emoji", "emoji": "🎓"},
            "parent": {"type": "workspace", "workspace": True},
            "archived": False,
            "in_trash": False,
            "properties": {
                "title": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": "Academy", "link": None},
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default",
                            },
                            "plain_text": "Academy",
                            "href": None,
                        }
                    ],
                }
            },
            "url": "https://www.notion.so/Academy-ff799030eae64c818631ee2653f27af8",
            "public_url": None,
        },
    ]


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
def user_1(sync_session) -> User:
    user_1 = (
        sync_session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    return user_1


@pytest.fixture(
    params=[
        PageParent(type="page_id", page_id=uuid4()),
        WorkspaceParent(type="workspace", workspace=True),
    ]
)
def notion_search_result(request) -> NotionSearchResult:
    return NotionSearchResult(
        results=[
            NotionPage(
                id=uuid4(),
                created_time=datetime.now(),
                last_edited_time=datetime.now(),
                url="url",
                archived=False,
                in_trash=False,
                public_url=None,
                parent=request.param,
                cover=None,
                icon=None,
                properties=PageProps(
                    title=Title(
                        id="id_title",
                        type="title",
                        title=[
                            TitleItem(
                                type="text",
                                text=TextContent(
                                    content="title",
                                    link=None,
                                ),
                                annotations={},
                                plain_text="",
                            )
                        ],
                    )
                ),
            )
        ],
        has_more=False,
        next_cursor=None,
    )


@pytest.fixture(
    params=[
        DatabaseParent(type="database_id", database_id=uuid4()),
        BlockParent(type="block_id", block_id=uuid4()),
    ]
)
def notion_search_result_bad_parent(request) -> NotionSearchResult:
    return NotionSearchResult(
        results=[
            NotionPage(
                id=uuid4(),
                created_time=datetime.now(),
                last_edited_time=datetime.now(),
                url="url",
                archived=False,
                in_trash=False,
                public_url=None,
                parent=request.param,
                cover=None,
                icon=None,
                properties=PageProps(
                    title=Title(
                        id="id_title",
                        type="title",
                        title=[
                            TitleItem(
                                type="text",
                                text=TextContent(
                                    content="title",
                                    link=None,
                                ),
                                annotations={},
                                plain_text="",
                            )
                        ],
                    )
                ),
            )
        ],
        has_more=False,
        next_cursor=None,
    )
