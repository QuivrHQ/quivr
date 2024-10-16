from datetime import datetime
from typing import List, Tuple
from uuid import uuid4

import pytest
import pytest_asyncio
from quivr_core.models import KnowledgeStatus
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.modules.brain.entity.brain_entity import Brain
from quivr_api.modules.knowledge.dto.outputs import KnowledgeDTO, sort_knowledge_dtos
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB, KnowledgeSource
from quivr_api.modules.user.entity.user_identity import User

TestData = Tuple[Brain, List[KnowledgeDB]]


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
    results = (await session.exec(statement)).unique().all()
    assert results == []


@pytest.mark.asyncio(loop_scope="session")
async def test_knowledge_dto(session, user, brain, brain2, sync):
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
        brains=[brain2, brain],
        parent=folder,
        sync_file_id="file1",
        sync=sync,
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
    assert km_dto.metadata == km.metadata_  # type: ignore
    assert km_dto.parent
    assert km_dto.parent.id == folder.id
    # Syncs fields
    assert km_dto.sync_id == km.sync_id
    assert km_dto.sync_file_id == km.sync_file_id
    # Check brain_name order
    assert len(km_dto.brains) == 2
    assert km_dto.brains[1]["name"] > km_dto.brains[0]["name"]

    # Check folder to dto
    folder_dto = await folder.to_dto()
    assert folder_dto.brains[0] == brain.model_dump()
    assert folder_dto.children == [await km.to_dto()]


def test_sort_knowledge_dtos():
    user_id = uuid4()

    data_dict = {
        "extension": ".txt",
        "status": None,
        "user_id": user_id,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "brains": [],
        "source": KnowledgeSource.LOCAL,
        "source_link": "://test.txt",
        "sync_id": None,
        "sync_file_id": None,
        "parent": None,
        "children": [],
    }
    dtos = [
        KnowledgeDTO(id=uuid4(), is_folder=False, file_name=None, **data_dict),
        KnowledgeDTO(id=uuid4(), is_folder=False, file_name="B", **data_dict),
        KnowledgeDTO(id=uuid4(), is_folder=True, file_name="A", **data_dict),
        KnowledgeDTO(id=uuid4(), is_folder=True, file_name=None, **data_dict),
    ]

    sorted_dtos = sort_knowledge_dtos(dtos)

    # First element should be a folder with file_name="A"
    assert sorted_dtos[0].is_folder is True
    assert sorted_dtos[0].file_name == "A"
    # Second element should be a folder with file_name=None
    assert sorted_dtos[1].is_folder is True
    assert sorted_dtos[1].file_name is None
    # Third element should be a file with file_name="B"
    assert sorted_dtos[2].is_folder is False
    assert sorted_dtos[2].file_name == "B"
    # Fourth element should be a file with file_name=None
    assert sorted_dtos[3].is_folder is False
    assert sorted_dtos[3].file_name is None
