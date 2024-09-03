import asyncio
import os
from typing import List, Tuple
from uuid import uuid4

import pytest
import pytest_asyncio
import sqlalchemy
from quivr_api.modules.brain.entity.brain_entity import Brain, BrainType
from quivr_api.modules.knowledge.dto.inputs import KnowledgeStatus
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.modules.knowledge.entity.knowledge_brain import KnowledgeBrain
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.user.entity.user_identity import User
from quivr_api.vector.entity.vector import Vector
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import select, text
from sqlmodel.ext.asyncio.session import AsyncSession

pg_database_base_url = "postgres:postgres@localhost:54322/postgres"

TestData = Tuple[Brain, List[KnowledgeDB]]


@pytest.fixture(scope="session")
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


@pytest_asyncio.fixture
async def other_user(session: AsyncSession):
    sql = text(
        """
        INSERT INTO "auth"."users" ("instance_id", "id", "aud", "role", "email", "encrypted_password", "email_confirmed_at", "invited_at", "confirmation_token", "confirmation_sent_at", "recovery_token", "recovery_sent_at", "email_change_token_new", "email_change", "email_change_sent_at", "last_sign_in_at", "raw_app_meta_data", "raw_user_meta_data", "is_super_admin", "created_at", "updated_at", "phone", "phone_confirmed_at", "phone_change", "phone_change_token", "phone_change_sent_at", "email_change_token_current", "email_change_confirm_status", "banned_until", "reauthentication_token", "reauthentication_sent_at", "is_sso_user", "deleted_at") VALUES
        ('00000000-0000-0000-0000-000000000000', :id , 'authenticated', 'authenticated', 'other@quivr.app', '$2a$10$vwKX0eMLlrOZvxQEA3Vl4e5V4/hOuxPjGYn9QK1yqeaZxa.42Uhze', '2024-01-22 22:27:00.166861+00', NULL, '', NULL, 'e91d41043ca2c83c3be5a6ee7a4abc8a4f4fb1afc0a8453c502af931', '2024-03-05 16:22:13.780421+00', '', '', NULL, '2024-03-30 23:21:12.077887+00', '{"provider": "email", "providers": ["email"]}', '{}', NULL, '2024-01-22 22:27:00.158026+00', '2024-04-01 17:40:15.332205+00', NULL, NULL, '', '', NULL, '', 0, NULL, '', NULL, false, NULL);
        """
    )
    await session.execute(sql, params={"id": uuid4()})

    other_user = (
        await session.exec(select(User).where(User.email == "other@quivr.app"))
    ).one()
    return other_user


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


@pytest.mark.asyncio
async def test_updates_knowledge_status(session: AsyncSession, test_data: TestData):
    brain, knowledges = test_data
    assert brain.brain_id
    assert knowledges[0].id
    repo = KnowledgeRepository(session)
    await repo.update_status_knowledge(knowledges[0].id, KnowledgeStatus.ERROR)
    knowledge = await repo.get_knowledge_by_id(knowledges[0].id)
    assert knowledge.status == KnowledgeStatus.ERROR


@pytest.mark.asyncio
async def test_updates_knowledge_status_no_knowledge(
    session: AsyncSession, test_data: TestData
):
    brain, knowledges = test_data
    assert brain.brain_id
    assert knowledges[0].id
    repo = KnowledgeRepository(session)
    with pytest.raises(NoResultFound):
        await repo.update_status_knowledge(uuid4(), KnowledgeStatus.UPLOADED)


@pytest.mark.asyncio
async def test_update_knowledge_source_link(session: AsyncSession, test_data: TestData):
    brain, knowledges = test_data
    assert brain.brain_id
    assert knowledges[0].id
    repo = KnowledgeRepository(session)
    await repo.update_source_link_knowledge(knowledges[0].id, "new_source_link")
    knowledge = await repo.get_knowledge_by_id(knowledges[0].id)
    assert knowledge.source_link == "new_source_link"


@pytest.mark.asyncio
async def test_remove_knowledge_from_brain(session: AsyncSession, test_data: TestData):
    brain, knowledges = test_data
    assert brain.brain_id
    assert knowledges[0].id
    repo = KnowledgeRepository(session)
    knowledge = await repo.remove_knowledge_from_brain(knowledges[0].id, brain.brain_id)
    assert brain.brain_id not in [
        b.brain_id for b in await knowledge.awaitable_attrs.brains
    ]


@pytest.mark.asyncio
async def test_cascade_remove_knowledge_by_id(
    session: AsyncSession, test_data: TestData
):
    brain, knowledges = test_data
    assert brain.brain_id
    assert knowledges[0].id
    repo = KnowledgeRepository(session)
    await repo.remove_knowledge_by_id(knowledges[0].id)
    with pytest.raises(NoResultFound):
        await repo.get_knowledge_by_id(knowledges[0].id)

    query = select(KnowledgeBrain).where(
        KnowledgeBrain.knowledge_id == knowledges[0].id
    )
    result = await session.exec(query)
    knowledge_brain = result.first()
    assert knowledge_brain is None

    query = select(Vector).where(Vector.knowledge_id == knowledges[0].id)
    result = await session.exec(query)
    vector = result.first()
    assert vector is None


@pytest.mark.asyncio
async def test_remove_all_knowledges_from_brain(
    session: AsyncSession, test_data: TestData
):
    brain, knowledges = test_data
    assert brain.brain_id

    # supabase_client = get_supabase_client()
    # db = supabase_client
    # storage = db.storage.from_("quivr")

    # storage.upload(f"{brain.brain_id}/test_file_1", b"test_content")

    repo = KnowledgeRepository(session)
    service = KnowledgeService(repo)
    await repo.remove_all_knowledges_from_brain(brain.brain_id)
    knowledges = await service.get_all_knowledge_in_brain(brain.brain_id)
    assert len(knowledges) == 0

    # response = storage.list(path=f"{brain.brain_id}")
    # assert response == []
    # FIXME @aminediro &chloedia raise an error when trying to interact with storage UnboundLocalError: cannot access local variable 'response' where it is not associated with a value


@pytest.mark.asyncio
async def test_duplicate_sha1_knowledge_same_user(
    session: AsyncSession, test_data: TestData
):
    brain, [existing_knowledge, _] = test_data
    assert brain.brain_id
    assert existing_knowledge.id
    assert existing_knowledge.file_sha1
    repo = KnowledgeRepository(session)
    knowledge = KnowledgeDB(
        file_name="test_file_2",
        extension="txt",
        status="UPLOADED",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1=existing_knowledge.file_sha1,
        brains=[brain],
        user_id=existing_knowledge.user_id,
    )

    with pytest.raises(IntegrityError):  # FIXME: Should raise IntegrityError
        await repo.insert_knowledge(knowledge, brain.brain_id)


@pytest.mark.asyncio
async def test_duplicate_sha1_knowledge_diff_user(
    session: AsyncSession, test_data: TestData, other_user: User
):
    brain, knowledges = test_data
    assert other_user.id
    assert brain.brain_id
    assert knowledges[0].id
    repo = KnowledgeRepository(session)
    knowledge = KnowledgeDB(
        file_name="test_file_2",
        extension="txt",
        status="UPLOADED",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1=knowledges[0].file_sha1,
        brains=[brain],
        user_id=other_user.id,  # random user id
    )

    result = await repo.insert_knowledge(knowledge, brain.brain_id)
    assert result


@pytest.mark.asyncio
async def test_add_knowledge_to_brain(session: AsyncSession, test_data: TestData):
    brain, knowledges = test_data
    assert brain.brain_id
    assert knowledges[1].id
    repo = KnowledgeRepository(session)
    await repo.link_to_brain(knowledges[1], brain.brain_id)
    knowledge = await repo.get_knowledge_by_id(knowledges[1].id)
    brains_of_knowledge = [b.brain_id for b in await knowledge.awaitable_attrs.brains]
    assert brain.brain_id in brains_of_knowledge

    query = select(KnowledgeBrain).where(
        KnowledgeBrain.knowledge_id == knowledges[0].id
        and KnowledgeBrain.brain_id == brain.brain_id
    )
    result = await session.exec(query)
    knowledge_brain = result.first()
    assert knowledge_brain


# Knowledge Service
@pytest.mark.asyncio
async def test_get_knowledge_in_brain(session: AsyncSession, test_data: TestData):
    brain, knowledges = test_data
    assert brain.brain_id
    repo = KnowledgeRepository(session)
    service = KnowledgeService(repo)
    list_knowledge = await service.get_all_knowledge_in_brain(brain.brain_id)
    assert len(list_knowledge) == 1
    brains_of_knowledge = [
        b.brain_id for b in await knowledges[0].awaitable_attrs.brains
    ]
    assert list_knowledge[0].id == knowledges[0].id
    assert list_knowledge[0].file_name == knowledges[0].file_name
    assert brain.brain_id in brains_of_knowledge


@pytest.mark.asyncio
async def test_should_process_knowledge_exists(
    session: AsyncSession, test_data: TestData
):
    brain, [existing_knowledge, _] = test_data
    assert brain.brain_id
    new = KnowledgeDB(
        file_name="new",
        extension="txt",
        status="PROCESSING",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1=None,
        brains=[brain],
        user_id=existing_knowledge.user_id,
    )
    session.add(new)
    await session.commit()
    await session.refresh(new)
    incoming_knowledge = await new.to_dto()
    repo = KnowledgeRepository(session)
    service = KnowledgeService(repo)
    assert existing_knowledge.file_sha1
    with pytest.raises(FileExistsError):
        await service.update_sha1_conflict(
            incoming_knowledge, brain.brain_id, file_sha1=existing_knowledge.file_sha1
        )


@pytest.mark.asyncio
async def test_should_process_knowledge_link_brain(
    session: AsyncSession, test_data: TestData
):
    repo = KnowledgeRepository(session)
    service = KnowledgeService(repo)
    brain, [existing_knowledge, _] = test_data
    user_id = existing_knowledge.user_id
    assert brain.brain_id
    prev = KnowledgeDB(
        file_name="prev",
        extension="txt",
        status=KnowledgeStatus.UPLOADED,
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1="test1",
        brains=[brain],
        user_id=user_id,
    )
    brain_2 = Brain(
        name="test_brain",
        description="this is a test brain",
        brain_type=BrainType.integration,
    )
    session.add(brain_2)
    session.add(prev)
    await session.commit()
    await session.refresh(prev)
    await session.refresh(brain_2)

    assert prev.id
    assert brain_2.brain_id

    new = KnowledgeDB(
        file_name="new",
        extension="txt",
        status="PROCESSING",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1=None,
        brains=[brain_2],
        user_id=user_id,
    )
    session.add(new)
    await session.commit()
    await session.refresh(new)

    incoming_knowledge = await new.to_dto()
    assert prev.file_sha1

    should_process = await service.update_sha1_conflict(
        incoming_knowledge, brain_2.brain_id, file_sha1=prev.file_sha1
    )
    assert not should_process

    # Check prev knowledge was linked
    assert incoming_knowledge.file_sha1
    prev_knowledge = await service.repository.get_knowledge_by_id(prev.id)
    prev_brains = await prev_knowledge.awaitable_attrs.brains
    assert {b.brain_id for b in prev_brains} == {
        brain.brain_id,
        brain_2.brain_id,
    }
    # Check new knowledge was removed
    assert new.id
    with pytest.raises(NoResultFound):
        await service.repository.get_knowledge_by_id(new.id)


@pytest.mark.asyncio
async def test_should_process_knowledge_prev_error(
    session: AsyncSession, test_data: TestData
):
    repo = KnowledgeRepository(session)
    service = KnowledgeService(repo)
    brain, [existing_knowledge, _] = test_data
    user_id = existing_knowledge.user_id
    assert brain.brain_id
    prev = KnowledgeDB(
        file_name="prev",
        extension="txt",
        status=KnowledgeStatus.ERROR,
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1="test1",
        brains=[brain],
        user_id=user_id,
    )
    session.add(prev)
    await session.commit()
    await session.refresh(prev)

    assert prev.id

    new = KnowledgeDB(
        file_name="new",
        extension="txt",
        status="PROCESSING",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1=None,
        brains=[brain],
        user_id=user_id,
    )
    session.add(new)
    await session.commit()
    await session.refresh(new)

    incoming_knowledge = await new.to_dto()
    assert prev.file_sha1
    should_process = await service.update_sha1_conflict(
        incoming_knowledge, brain.brain_id, file_sha1=prev.file_sha1
    )

    # Checks we should process this file
    assert should_process
    # Previous errored file is cleaned up
    with pytest.raises(NoResultFound):
        await service.repository.get_knowledge_by_id(prev.id)

    assert new.id
    new = await service.repository.get_knowledge_by_id(new.id)
    assert new.file_sha1
