import asyncio
import os
from typing import List, Tuple
from uuid import uuid4

import pytest
import pytest_asyncio
import sqlalchemy
from quivr_api.celery_config import celery
from quivr_api.modules.brain.entity.brain_entity import Brain, BrainType
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.modules.user.entity.user_identity import User
from quivr_worker.parsers.crawler import URL, extract_from_url
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

pg_database_base_url = "postgres:postgres@localhost:54322/postgres"

async_engine = create_async_engine(
    "postgresql+asyncpg://" + pg_database_base_url,
    echo=True if os.getenv("ORM_DEBUG") else False,
    future=True,
    pool_pre_ping=True,
    pool_size=10,
    pool_recycle=0.1,
)


TestData = Tuple[Brain, List[KnowledgeDB]]


@pytest_asyncio.fixture(scope="function")
async def session():
    print("\nSESSION_EVEN_LOOP", id(asyncio.get_event_loop()))
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


@pytest_asyncio.fixture()
async def test_data(session: AsyncSession) -> TestData:
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    assert user_1.id
    # Brain data
    brain_1 = Brain(
        name="test_brain",
        description="this is a test brain",
        brain_type=BrainType.integration,
    )

    knowledge_brain_1 = KnowledgeDB(
        file_name="test_file_1",
        extension="txt",
        status="UPLOADED",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1="test_sha1",
        brains=[brain_1],
        user_id=user_1.id,
    )

    knowledge_brain_2 = KnowledgeDB(
        file_name="test_file_2",
        extension="txt",
        status="UPLOADED",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1="test_sha2",
        brains=[],
        user_id=user_1.id,
    )

    session.add(brain_1)
    session.add(knowledge_brain_1)
    session.add(knowledge_brain_2)
    await session.commit()
    return brain_1, [knowledge_brain_1, knowledge_brain_2]


@pytest.mark.skip
def test_crawl():
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    crawl_website = URL(url=url)
    extracted_content = extract_from_url(crawl_website)

    assert len(extracted_content) > 1


@pytest.mark.skip
def test_process_crawl_task(test_data: TestData):
    brain, [knowledge, _] = test_data
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    task = celery.send_task(
        "process_crawl_task",
        kwargs={
            "crawl_website_url": url,
            "brain_id": brain.brain_id,
            "knowledge_id": knowledge.id,
            "notification_id": uuid4(),
        },
    )
    result = task.wait()  # noqa: F841
