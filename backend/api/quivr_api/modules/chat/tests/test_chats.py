import asyncio
import os
from typing import List, Tuple
from uuid import uuid4

import pytest
import pytest_asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.modules.brain.entity.brain_entity import Brain, BrainType
from quivr_api.modules.chat.dto.inputs import QuestionAndAnswer
from quivr_api.modules.chat.entity.chat import Chat, ChatHistory
from quivr_api.modules.chat.repository.chats import ChatRepository
from quivr_api.modules.chat.service.chat_service import ChatService
from quivr_api.modules.user.entity.user_identity import User

pg_database_base_url = "postgres:postgres@localhost:54322/postgres"

TestData = Tuple[Brain, User, List[Chat], List[ChatHistory]]


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


@pytest_asyncio.fixture()
async def test_data(
    session: AsyncSession,
) -> TestData:
    # User data
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    # Brain data
    brain_1 = Brain(
        name="test_brain",
        description="this is a test brain",
        brain_type=BrainType.integration,
    )
    # Chat data
    chat_1 = Chat(chat_name="chat1", user=user_1)
    chat_2 = Chat(chat_name="chat2", user=user_1)

    chat_history_1 = ChatHistory(
        user_message="Hello",
        assistant="Hello! How can I assist you today?",
        chat=chat_1,
        brain=brain_1,
    )
    chat_history_2 = ChatHistory(
        user_message="Hello",
        assistant="Hello! How can I assist you today?",
        chat=chat_1,
        brain=brain_1,
    )
    session.add(brain_1)
    session.add(chat_1)
    session.add(chat_2)
    session.add(chat_history_1)
    session.add(chat_history_2)

    await session.refresh(user_1)
    await session.commit()
    return brain_1, user_1, [chat_1, chat_2], [chat_history_1, chat_history_2]


@pytest.mark.asyncio
async def test_get_user_chats_empty(session):
    repo = ChatRepository(session)
    chats = await repo.get_user_chats(user_id=uuid4())
    assert len(chats) == 0


@pytest.mark.asyncio
async def test_get_user_chats(session: AsyncSession, test_data: TestData):
    _, local_user, chats, _ = test_data
    repo = ChatRepository(session)
    assert local_user.id is not None
    query_chats = await repo.get_user_chats(local_user.id)
    assert len(query_chats) == len(chats)


@pytest.mark.asyncio
async def test_get_chat_history_close(session: AsyncSession, test_data: TestData):
    brain_1, _, chats, chat_history = test_data
    assert chats[0].chat_id
    assert len(chat_history) > 0
    assert chat_history[-1].message_time
    assert chat_history[0].message_time


@pytest.mark.asyncio
async def test_get_chat_history(session: AsyncSession, test_data: TestData):
    brain_1, _, chats, chat_history = test_data
    assert chats[0].chat_id
    assert len(chat_history) > 0
    assert chat_history[-1].message_time
    assert chat_history[0].message_time

    repo = ChatRepository(session)
    query_chat_history = await repo.get_chat_history(chats[0].chat_id)
    assert chat_history == query_chat_history
    assert query_chat_history[-1].message_time
    assert query_chat_history[0].message_time
    assert query_chat_history[-1].message_time >= query_chat_history[0].message_time

    # TODO: Should be tested in test_brain_repository
    # Checks that brain is correct
    assert query_chat_history[-1].brain is not None
    assert query_chat_history[-1].brain.brain_type == BrainType.integration


@pytest.mark.asyncio
async def test_add_qa(session: AsyncSession, test_data: TestData):
    _, _, [chat, *_], __ = test_data
    assert chat.chat_id
    qa = QuestionAndAnswer(question="question", answer="answer")
    repo = ChatRepository(session)
    resp_chat = await repo.add_question_and_answer(chat.chat_id, qa)

    assert resp_chat.chat_id == chat.chat_id
    assert resp_chat.user_message == qa.question
    assert resp_chat.assistant == qa.answer


# CHAT SERVICE


@pytest.mark.asyncio
async def test_service_get_chat_history(session: AsyncSession, test_data: TestData):
    brain, _, [chat, *_], __ = test_data
    assert chat.chat_id
    repo = ChatRepository(session)
    service = ChatService(repo)
    history = await service.get_chat_history(chat.chat_id)

    assert len(history) > 0
    assert all(h.chat_id == chat.chat_id for h in history)
    assert history[0].brain_name == brain.name
    assert history[0].brain_id == brain.brain_id
