from typing import List, Tuple
from uuid import uuid4

import pytest
import pytest_asyncio
from quivr_core.models import KnowledgeStatus
from sqlmodel import select, text
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.modules.brain.entity.brain_entity import Brain, BrainType
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.modules.user.entity.user_identity import User

TestData = Tuple[Brain, List[KnowledgeDB]]


@pytest_asyncio.fixture(scope="function")
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


@pytest_asyncio.fixture(scope="function")
async def user(session):
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    return user_1


@pytest_asyncio.fixture(scope="function")
async def brain(session):
    brain_1 = Brain(
        name="test_brain",
        description="this is a test brain",
        brain_type=BrainType.integration,
    )
    session.add(brain_1)
    await session.commit()
    return brain_1


@pytest_asyncio.fixture(scope="function")
async def folder(session, user):
    folder = KnowledgeDB(
        file_name="folder_1",
        extension="",
        status="UPLOADED",
        source="local",
        source_link="local",
        file_size=4,
        file_sha1=None,
        brains=[],
        children=[],
        user_id=user.id,
        is_folder=True,
    )

    session.add(folder)
    await session.commit()
    await session.refresh(folder)
    return folder


@pytest.mark.asyncio(loop_scope="session")
async def test_knowledge_default_file(session, folder, user):
    km = KnowledgeDB(
        file_name="test_file_1.txt",
        extension=".txt",
        status="UPLOADED",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1="test_sha1",
        brains=[],
        user_id=user.id,
        parent_id=folder.id,
    )
    session.add(km)
    await session.commit()
    await session.refresh(km)

    assert not km.is_folder


@pytest.mark.asyncio(loop_scope="session")
async def test_knowledge_parent(session: AsyncSession, user: User):
    assert user.id

    km = KnowledgeDB(
        file_name="test_file_1.txt",
        extension=".txt",
        status="UPLOADED",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1="test_sha1",
        brains=[],
        user_id=user.id,
    )

    folder = KnowledgeDB(
        file_name="folder_1",
        extension="",
        is_folder=True,
        status="UPLOADED",
        source="local",
        source_link="local",
        file_size=-1,
        file_sha1=None,
        brains=[],
        children=[km],
        user_id=user.id,
    )

    session.add(folder)
    await session.commit()
    await session.refresh(folder)
    await session.refresh(km)

    parent = await km.awaitable_attrs.parent
    assert km.parent_id == folder.id, "parent_id isn't set to folder id"
    assert parent.id == folder.id, "parent_id isn't set to folder id"
    assert parent.is_folder

    query = select(KnowledgeDB).where(KnowledgeDB.id == folder.id)
    folder = (await session.exec(query)).first()
    assert folder

    children = await folder.awaitable_attrs.children
    assert len(children) > 0

    assert children[0].id == km.id


@pytest.mark.asyncio(loop_scope="session")
async def test_knowledge_remove_folder_cascade(
    session: AsyncSession,
    folder: KnowledgeDB,
    user,
):
    km = KnowledgeDB(
        file_name="test_file_1.txt",
        extension=".txt",
        status="UPLOADED",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1="test_sha1",
        brains=[],
        user_id=user.id,
        parent_id=folder.id,
    )
    session.add(km)
    await session.commit()
    await session.refresh(km)

    # Check all removed
    await session.delete(folder)
    await session.commit()

    statement = select(KnowledgeDB)
    results = (await session.exec(statement)).all()
    assert results == []


@pytest.mark.asyncio(loop_scope="session")
async def test_knowledge_dto(session, user, brain):
    # add folder in brain
    folder = KnowledgeDB(
        file_name="folder_1",
        extension="",
        status="UPLOADED",
        source="local",
        source_link="local",
        file_size=4,
        file_sha1=None,
        brains=[brain],
        children=[],
        user_id=user.id,
        is_folder=True,
    )
    km = KnowledgeDB(
        file_name="test_file_1.txt",
        extension=".txt",
        status="UPLOADED",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1="test_sha1",
        user_id=user.id,
        brains=[brain],
        parent=folder,
    )
    session.add(km)
    session.add(km)
    await session.commit()
    await session.refresh(km)

    km_dto = await km.to_dto()

    assert km_dto.file_name == km.file_name
    assert km_dto.url == km.url
    assert km_dto.extension == km.extension
    assert km_dto.status == KnowledgeStatus(km.status)
    assert km_dto.source == km.source
    assert km_dto.source_link == km.source_link
    assert km_dto.is_folder == km.is_folder
    assert km_dto.file_size == km.file_size
    assert km_dto.file_sha1 == km.file_sha1
    assert km_dto.updated_at == km.updated_at
    assert km_dto.created_at == km.created_at
    assert km_dto.metadata == km.metadata_  # type: ignor
    assert km_dto.parent
    assert km_dto.parent.id == folder.id

    folder_dto = await folder.to_dto()
    assert folder_dto.brains[0] == brain.model_dump()
    assert folder_dto.children == [await km.to_dto()]
