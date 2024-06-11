import asyncio
from typing import List, Tuple
from uuid import uuid4

import pytest
import pytest_asyncio
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import create_engine, select
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.modules.chat.dto.inputs import QuestionAndAnswer
from backend.modules.chat.entity.chat import Chat, ChatHistory
from backend.modules.chat.repository.chats import ChatRepository
from backend.modules.user.entity.user_identity import User

pg_database_url = "postgres:postgres@localhost:54322/postgres"


@pytest.fixture(scope="session", autouse=True)
def db_setup():
    # setup
    sync_engine = create_engine("postgresql://" + pg_database_url, echo=True)
    #  TODO(@amine) : for now don't drop anything
    yield sync_engine
    # teardown
    # NOTE: For now we rely on Supabase migrations for defining schemas
    # SQLModel.metadata.create_all(sync_engine, checkfirst=True)
    # SQLModel.metadata.drop_all(sync_engine)


@pytest_asyncio.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(
        "postgresql+asyncpg://" + pg_database_url,
        echo=True,  # future=True
    )
    yield engine


@pytest.fixture(scope="session")
def event_loop(request: pytest.FixtureRequest):
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


TestData = Tuple[User, List[Chat], List[ChatHistory]]


@pytest_asyncio.fixture()
async def test_data(
    session: AsyncSession,
) -> TestData:
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    chat_1 = Chat(chat_name="chat1", user=user_1)
    chat_2 = Chat(chat_name="chat2", user=user_1)

    chat_history_1 = ChatHistory(
        user_message="Hello",
        assistant="Hello! How can I assist you today?",
        chat=chat_1,
    )
    chat_history_2 = ChatHistory(
        user_message="Hello",
        assistant="Hello! How can I assist you today?",
        chat=chat_1,
    )
    session.add(chat_1)
    session.add(chat_2)
    session.add(chat_history_1)
    session.add(chat_history_2)

    await session.refresh(user_1)
    await session.commit()
    return user_1, [chat_1, chat_2], [chat_history_1, chat_history_2]


@pytest.mark.asyncio
async def test_get_user_chats_empty(session):
    repo = ChatRepository(session)
    chats = await repo.get_user_chats(user_id=uuid4())
    assert len(chats) == 0


@pytest.mark.asyncio
async def test_get_user_chats(session: AsyncSession, test_data: TestData):
    local_user, chats, _ = test_data
    repo = ChatRepository(session)
    assert local_user.id is not None
    query_chats = await repo.get_user_chats(local_user.id)
    assert len(query_chats) == len(chats)


@pytest.mark.asyncio
async def test_get_chat_history(session: AsyncSession, test_data: TestData):
    _, chats, chat_history = test_data
    assert chats[0].chat_id
    assert len(chat_history) > 0
    assert chat_history[-1].message_time
    assert chat_history[0].message_time

    repo = ChatRepository(session)
    query_chat_history = await repo.get_chat_history(chats[0].chat_id)
    assert chat_history == query_chat_history
    assert query_chat_history[-1].message_time >= query_chat_history[0].message_time


@pytest.mark.asyncio
async def test_add_qa(session: AsyncSession, test_data: TestData):
    _, [chat, *_], __ = test_data
    assert chat.chat_id
    qa = QuestionAndAnswer(question="question", answer="answer")
    repo = ChatRepository(session)
    chat = await repo.add_question_and_answer(chat.chat_id, qa)

    assert chat.user_message == qa.question
    assert chat.assistant == qa.answer
