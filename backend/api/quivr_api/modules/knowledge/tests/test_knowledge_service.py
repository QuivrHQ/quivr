import os
from io import BytesIO
from typing import List, Tuple
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import UploadFile
from sqlalchemy.exc import NoResultFound
from sqlmodel import select, text
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.modules.brain.entity.brain_entity import Brain, BrainType
from quivr_api.modules.knowledge.dto.inputs import AddKnowledge, KnowledgeStatus
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB, KnowledgeUpdate
from quivr_api.modules.knowledge.entity.knowledge_brain import KnowledgeBrain
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.service.knowledge_exceptions import (
    KnowledgeNotFoundException,
    KnowledgeUpdateError,
    UploadError,
)
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.knowledge.tests.conftest import ErrorStorage, FakeStorage
from quivr_api.modules.upload.service.upload_file import upload_file_storage
from quivr_api.modules.user.entity.user_identity import User
from quivr_api.modules.vector.entity.vector import Vector

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
async def user(session: AsyncSession) -> User:
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    assert user_1.id
    return user_1


@pytest_asyncio.fixture(scope="function")
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
        file_name="test_file_1.txt",
        extension=".txt",
        status="UPLOADED",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1="test_sha1",
        brains=[brain_1],
        user_id=user_1.id,
    )

    knowledge_brain_2 = KnowledgeDB(
        file_name="test_file_2.txt",
        extension=".txt",
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


@pytest_asyncio.fixture(scope="function")
async def folder_km_nested(session: AsyncSession, user: User):
    assert user.id

    nested_folder = KnowledgeDB(
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
    folder = KnowledgeDB(
        file_name="folder_2",
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
        parent=nested_folder,
    )

    knowledge_folder = KnowledgeDB(
        file_name="file.txt",
        extension=".txt",
        status="UPLOADED",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1="test_sha2",
        brains=[],
        user_id=user.id,
        parent=folder,
    )

    session.add(nested_folder)
    session.add(folder)
    session.add(knowledge_folder)
    await session.commit()
    await session.refresh(folder)
    return nested_folder


@pytest_asyncio.fixture(scope="function")
async def folder_km(session: AsyncSession, user: User):
    assert user.id
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

    knowledge_folder = KnowledgeDB(
        file_name="file.txt",
        extension=".txt",
        status="UPLOADED",
        source="test_source",
        source_link="test_source_link",
        file_size=100,
        file_sha1="test_sha2",
        brains=[],
        user_id=user.id,
        parent=folder,
    )

    session.add(folder)
    session.add(knowledge_folder)
    await session.commit()
    await session.refresh(folder)
    return folder


@pytest.mark.asyncio(loop_scope="session")
async def test_updates_knowledge_status(session: AsyncSession, test_data: TestData):
    brain, knowledges = test_data
    assert brain.brain_id
    assert knowledges[0].id
    repo = KnowledgeRepository(session)
    await repo.update_status_knowledge(knowledges[0].id, KnowledgeStatus.ERROR)
    knowledge = await repo.get_knowledge_by_id(knowledges[0].id)
    assert knowledge.status == KnowledgeStatus.ERROR


@pytest.mark.asyncio(loop_scope="session")
async def test_updates_knowledge_status_no_knowledge(
    session: AsyncSession, test_data: TestData
):
    brain, knowledges = test_data
    assert brain.brain_id
    assert knowledges[0].id
    repo = KnowledgeRepository(session)
    with pytest.raises(NoResultFound):
        await repo.update_status_knowledge(uuid4(), KnowledgeStatus.UPLOADED)


@pytest.mark.asyncio(loop_scope="session")
async def test_update_knowledge_source_link(session: AsyncSession, test_data: TestData):
    brain, knowledges = test_data
    assert brain.brain_id
    assert knowledges[0].id
    repo = KnowledgeRepository(session)
    await repo.update_source_link_knowledge(knowledges[0].id, "new_source_link")
    knowledge = await repo.get_knowledge_by_id(knowledges[0].id)
    assert knowledge.source_link == "new_source_link"


@pytest.mark.asyncio(loop_scope="session")
async def test_remove_knowledge_from_brain(session: AsyncSession, test_data: TestData):
    brain, knowledges = test_data
    assert brain.brain_id
    assert knowledges[0].id
    repo = KnowledgeRepository(session)
    knowledge = await repo.remove_knowledge_from_brain(knowledges[0].id, brain.brain_id)
    assert brain.brain_id not in [
        b.brain_id for b in await knowledge.awaitable_attrs.brains
    ]


@pytest.mark.asyncio(loop_scope="session")
async def test_cascade_remove_knowledge_by_id(
    session: AsyncSession, test_data: TestData
):
    brain, knowledges = test_data
    assert brain.brain_id
    assert knowledges[0].id
    repo = KnowledgeRepository(session)
    await repo.remove_knowledge_by_id(knowledges[0].id)
    with pytest.raises(KnowledgeNotFoundException):
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


@pytest.mark.asyncio(loop_scope="session")
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


@pytest.mark.asyncio(loop_scope="session")
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

    await repo.insert_knowledge_brain(knowledge, brain.brain_id)


@pytest.mark.asyncio(loop_scope="session")
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

    result = await repo.insert_knowledge_brain(knowledge, brain.brain_id)
    assert result


@pytest.mark.asyncio(loop_scope="session")
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
@pytest.mark.asyncio(loop_scope="session")
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


@pytest.mark.asyncio(loop_scope="session")
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
    repo = KnowledgeRepository(session)
    service = KnowledgeService(repo)
    assert existing_knowledge.file_sha1
    with pytest.raises(FileExistsError):
        await service.update_sha1_conflict(
            new, brain.brain_id, file_sha1=existing_knowledge.file_sha1
        )


@pytest.mark.asyncio(loop_scope="session")
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
        extension=".txt",
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
    with pytest.raises(KnowledgeNotFoundException):
        await service.repository.get_knowledge_by_id(new.id)


@pytest.mark.asyncio(loop_scope="session")
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
    with pytest.raises(KnowledgeNotFoundException):
        await service.repository.get_knowledge_by_id(prev.id)

    assert new.id
    new = await service.repository.get_knowledge_by_id(new.id)
    assert new.file_sha1


@pytest.mark.skip(
    reason="Bug: UnboundLocalError: cannot access local variable 'response'"
)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_knowledge_storage_path(session: AsyncSession, test_data: TestData):
    _, [knowledge, _] = test_data
    assert knowledge.file_name
    repository = KnowledgeRepository(session)
    service = KnowledgeService(repository)
    brain_2 = Brain(
        name="test_brain",
        description="this is a test brain",
        brain_type=BrainType.integration,
    )
    session.add(brain_2)
    await session.commit()
    await session.refresh(brain_2)
    assert brain_2.brain_id
    km_data = os.urandom(128)
    km_path = f"{str(knowledge.brains[0].brain_id)}/{knowledge.file_name}"
    await upload_file_storage(km_data, km_path)
    # Link knowledge to two brains
    await repository.link_to_brain(knowledge, brain_2.brain_id)
    storage_path = await service.get_knowledge_storage_path(
        knowledge.file_name, brain_2.brain_id
    )
    assert storage_path == km_path


@pytest.mark.asyncio(loop_scope="session")
async def test_create_knowledge_file(session: AsyncSession, user: User):
    assert user.id
    storage = FakeStorage()
    repository = KnowledgeRepository(session)
    service = KnowledgeService(repository, storage)

    km_to_add = AddKnowledge(
        file_name="test",
        source="local",
        is_folder=False,
        parent_id=None,
    )
    km_data = BytesIO(os.urandom(128))

    km = await service.create_knowledge(
        user_id=user.id,
        knowledge_to_add=km_to_add,
        upload_file=UploadFile(file=km_data, size=128, filename=km_to_add.file_name),
    )

    assert km.file_name == km_to_add.file_name
    assert km.id
    assert km.status == KnowledgeStatus.UPLOADED
    assert not km.is_folder
    # km in storage
    storage.knowledge_exists(km)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_knowledge_folder(session: AsyncSession, user: User):
    assert user.id
    storage = FakeStorage()
    repository = KnowledgeRepository(session)
    service = KnowledgeService(repository, storage)

    km_to_add = AddKnowledge(
        file_name="test",
        source="local",
        is_folder=True,
        parent_id=None,
    )
    km_data = BytesIO(os.urandom(128))

    km = await service.create_knowledge(
        user_id=user.id,
        knowledge_to_add=km_to_add,
        upload_file=UploadFile(file=km_data, size=128, filename=km_to_add.file_name),
    )

    assert km.file_name == km_to_add.file_name
    assert km.id
    # Knowledge properties
    assert km.file_name == km_to_add.file_name
    assert km.is_folder == km_to_add.is_folder
    assert km.url == km_to_add.url
    assert km.extension == km_to_add.extension
    assert km.source == km_to_add.source
    assert km.file_size == 128
    assert km.metadata_ == km_to_add.metadata
    assert km.is_folder == km_to_add.is_folder
    assert km.status == KnowledgeStatus.UPLOADED
    # Knowledge was saved
    assert storage.knowledge_exists(km)


@pytest.mark.asyncio(loop_scope="session")
async def test_create_knowledge_upload_error(session: AsyncSession, user: User):
    assert user.id
    storage = ErrorStorage()
    repository = KnowledgeRepository(session)
    service = KnowledgeService(repository, storage)

    km_to_add = AddKnowledge(
        file_name="test",
        source="local",
        is_folder=True,
        parent_id=None,
    )
    km_data = BytesIO(os.urandom(128))

    with pytest.raises(UploadError):
        await service.create_knowledge(
            user_id=user.id,
            knowledge_to_add=km_to_add,
            upload_file=UploadFile(
                file=km_data, size=128, filename=km_to_add.file_name
            ),
        )
    # Check removed knowledge
    statement = select(KnowledgeDB)
    results = (await session.exec(statement)).all()
    assert results == []


@pytest.mark.asyncio(loop_scope="session")
async def test_get_knowledge(session: AsyncSession, folder_km: KnowledgeDB, user: User):
    assert user.id
    assert folder_km.id
    storage = ErrorStorage()
    repository = KnowledgeRepository(session)
    service = KnowledgeService(repository, storage)

    result = await service.get_knowledge(folder_km.id)
    assert result.id == folder_km.id
    assert result.children
    assert len(result.children) > 0
    assert result.children[0] == folder_km.children[0]


@pytest.mark.asyncio(loop_scope="session")
async def test_get_knowledge_nested(
    session: AsyncSession, folder_km_nested: KnowledgeDB, user: User
):
    assert user.id
    assert folder_km_nested.id
    storage = ErrorStorage()
    repository = KnowledgeRepository(session)
    service = KnowledgeService(repository, storage)

    result = await service.get_knowledge(folder_km_nested.id)
    assert result.id == folder_km_nested.id
    assert result.children
    assert len(result.children) > 0
    assert result.children[0].is_folder
    assert result.children[0] == folder_km_nested.children[0]


@pytest.mark.asyncio(loop_scope="session")
async def test_update_knowledge_rename(
    session: AsyncSession, folder_km: KnowledgeDB, user: User
):
    assert user.id
    assert folder_km.id
    storage = ErrorStorage()
    repository = KnowledgeRepository(session)
    service = KnowledgeService(repository, storage)

    new_km = await service.update_knowledge(
        folder_km,
        KnowledgeUpdate(file_name="change_name"),  # type: ignore
    )
    assert new_km.file_name == "change_name"


@pytest.mark.asyncio(loop_scope="session")
async def test_update_knowledge_move(
    session: AsyncSession, folder_km: KnowledgeDB, user: User
):
    assert user.id
    assert folder_km.id
    folder_2 = KnowledgeDB(
        file_name="folder_2",
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
    session.add(folder_2)
    await session.commit()
    await session.refresh(folder_2)

    storage = FakeStorage()
    repository = KnowledgeRepository(session)
    service = KnowledgeService(repository, storage)

    new_km = await service.update_knowledge(
        folder_km,
        KnowledgeUpdate(parent_id=folder_2.id),  # type: ignore
    )
    assert new_km.parent_id == folder_2.id


@pytest.mark.asyncio(loop_scope="session")
async def test_update_knowledge_move_error(session: AsyncSession, user: User):
    assert user.id
    file_1 = KnowledgeDB(
        file_name="file_1",
        extension="",
        status="UPLOADED",
        source="local",
        source_link="local",
        file_size=4,
        file_sha1=None,
        brains=[],
        children=[],
        user_id=user.id,
        is_folder=False,
    )
    file_2 = KnowledgeDB(
        file_name="file_2",
        extension="",
        status="UPLOADED",
        source="local",
        source_link="local",
        file_size=4,
        file_sha1=None,
        brains=[],
        children=[],
        user_id=user.id,
        is_folder=False,
    )
    session.add(file_1)
    session.add(file_2)
    await session.commit()
    await session.refresh(file_1)
    await session.refresh(file_2)

    storage = FakeStorage()
    repository = KnowledgeRepository(session)
    service = KnowledgeService(repository, storage)

    with pytest.raises(KnowledgeUpdateError):
        await service.update_knowledge(
            file_2,
            KnowledgeUpdate(parent_id=file_1.id),  # type: ignore
        )


@pytest.mark.asyncio(loop_scope="session")
async def test_update_knowledge_multiple(session: AsyncSession, user: User):
    assert user.id
    file = KnowledgeDB(
        file_name="file",
        extension="",
        status="UPLOADED",
        source="local",
        source_link="local",
        file_size=None,
        file_sha1=None,
        user_id=user.id,
    )
    folder = KnowledgeDB(
        file_name="folder_2",
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
    session.add(file)
    session.add(folder)
    await session.commit()
    await session.refresh(folder)

    storage = ErrorStorage()
    repository = KnowledgeRepository(session)
    service = KnowledgeService(repository, storage)

    await service.update_knowledge(
        file,
        KnowledgeUpdate(parent_id=folder.id, status="UPLOADED", file_sha1="sha1"),  # type: ignore
    )

    km = (
        await session.exec(select(KnowledgeDB).where(KnowledgeDB.id == file.id))
    ).first()
    assert km
    assert km.parent_id == folder.id
    assert km.status == "UPLOADED"
    assert km.file_sha1 == "sha1"


@pytest.mark.asyncio(loop_scope="session")
async def test_remove_knowledge(session: AsyncSession, user: User):
    assert user.id
    storage = FakeStorage()
    repository = KnowledgeRepository(session)
    service = KnowledgeService(repository, storage)

    km_to_add = AddKnowledge(
        file_name="test",
        source="local",
        is_folder=False,
        parent_id=None,
    )
    km_data = BytesIO(os.urandom(128))

    # Create the knowledge
    km = await service.create_knowledge(
        user_id=user.id,
        knowledge_to_add=km_to_add,
        upload_file=UploadFile(file=km_data, size=128, filename=km_to_add.file_name),
    )

    # Remove knowledge
    response = await service.remove_knowledge(knowledge=km)

    assert response.knowledge_id == km.id
    assert response.file_name == km.file_name

    assert not storage.knowledge_exists(km)
    assert (
        await session.exec(select(KnowledgeDB).where(KnowledgeDB.id == km.id))
    ).first() is None


@pytest.mark.asyncio(loop_scope="session")
async def test_remove_knowledge_folder(session: AsyncSession, user: User):
    assert user.id
    storage = FakeStorage()
    repository = KnowledgeRepository(session)
    service = KnowledgeService(repository, storage)

    folder_add = AddKnowledge(
        file_name="folder",
        source="local",
        is_folder=True,
        parent_id=None,
    )

    # Create the knowledge
    folder = await service.create_knowledge(
        user_id=user.id, knowledge_to_add=folder_add, upload_file=None
    )
    file_add = AddKnowledge(
        file_name="file",
        source="local",
        is_folder=False,
        parent_id=folder.id,
    )

    km_data = BytesIO(os.urandom(128))
    file = await service.create_knowledge(
        user_id=user.id,
        knowledge_to_add=file_add,
        upload_file=UploadFile(file=km_data, size=128, filename=file_add.file_name),
    )
    assert storage.knowledge_exists(file)

    # Remove knowledge
    await service.remove_knowledge(knowledge=folder)

    assert not storage.knowledge_exists(folder)
    assert not storage.knowledge_exists(file)
    assert (
        await session.exec(select(KnowledgeDB).where(KnowledgeDB.id == folder.id))
    ).first() is None
    assert (
        await session.exec(select(KnowledgeDB).where(KnowledgeDB.id == file.id))
    ).first() is None


@pytest.mark.asyncio(loop_scope="session")
async def test_list_knowledge_root(session: AsyncSession, user: User):
    assert user.id
    root_file = KnowledgeDB(
        file_name="file_1",
        extension="",
        status="UPLOADED",
        source="local",
        source_link="local",
        file_size=None,
        file_sha1=None,
        user_id=user.id,
    )

    root_folder = KnowledgeDB(
        file_name="folder",
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
    nested_file = KnowledgeDB(
        file_name="file_2",
        extension="",
        status="UPLOADED",
        source="local",
        source_link="local",
        file_size=10,
        file_sha1=None,
        user_id=user.id,
        parent=root_folder,
    )
    session.add(nested_file)
    session.add(root_file)
    session.add(root_folder)
    await session.commit()
    await session.refresh(root_folder)
    await session.refresh(root_file)
    await session.refresh(nested_file)

    storage = FakeStorage()
    repository = KnowledgeRepository(session)
    service = KnowledgeService(repository, storage)

    root_kms = await service.list_knowledge(knowledge_id=None, user_id=user.id)

    assert len(root_kms) == 2
    assert {k.id for k in root_kms} == {root_folder.id, root_file.id}


@pytest.mark.asyncio(loop_scope="session")
async def test_list_knowledge(session: AsyncSession, user: User):
    assert user.id
    root_file = KnowledgeDB(
        file_name="file_1",
        extension="",
        status="UPLOADED",
        source="local",
        source_link="local",
        file_size=None,
        file_sha1=None,
        user_id=user.id,
    )

    root_folder = KnowledgeDB(
        file_name="folder",
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
    nested_file = KnowledgeDB(
        file_name="file_2",
        extension="",
        status="UPLOADED",
        source="local",
        source_link="local",
        file_size=10,
        file_sha1=None,
        user_id=user.id,
        parent=root_folder,
    )
    session.add(nested_file)
    session.add(root_file)
    session.add(root_folder)
    await session.commit()
    await session.refresh(root_folder)
    await session.refresh(root_file)
    await session.refresh(nested_file)

    storage = FakeStorage()
    repository = KnowledgeRepository(session)
    service = KnowledgeService(repository, storage)

    kms = await service.list_knowledge(knowledge_id=root_folder.id, user_id=user.id)

    assert len(kms) == 1
    assert kms[0].id == nested_file.id
