from typing import Any

import pytest
from langchain_core.documents import Document
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.modules.vector.entity.vector import Vector
from quivr_core.files.file import QuivrFile
from quivr_core.models import KnowledgeStatus
from quivr_worker.process.processor import KnowledgeProcessor, ProcessorServices
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("proc_services", [0], indirect=True)
async def test_process_local_file(
    monkeypatch,
    session: AsyncSession,
    km_processor: KnowledgeProcessor,
    local_knowledge_file: KnowledgeDB,
):
    async def _parse_file_mock(
        qfile: QuivrFile,
        **processor_kwargs: dict[str, Any],
    ) -> list[Document]:
        with open(qfile.path, "rb") as f:
            return [Document(page_content=str(f.read()), metadata={})]

    monkeypatch.setattr("quivr_worker.process.processor.parse_qfile", _parse_file_mock)
    km_dto = await local_knowledge_file.to_dto(get_children=False, get_parent=False)
    await km_processor.process_knowledge(km_dto)

    # Check knowledge set to processed
    assert km_dto.id
    assert km_dto.brains
    knowledge_service = km_processor.services.knowledge_service
    km = await knowledge_service.get_knowledge(km_dto.id)
    assert km.status == KnowledgeStatus.PROCESSED
    assert km.brains[0].brain_id == km_dto.brains[0]["brain_id"]

    # Check vectors where added
    vecs = list(
        (
            await session.exec(
                select(Vector).where(col(Vector.knowledge_id) == km_dto.id)
            )
        ).all()
    )
    assert len(vecs) > 0
    assert vecs[0].metadata_ is not None


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("proc_services", [0], indirect=True)
async def test_process_sync_file(
    monkeypatch,
    session: AsyncSession,
    proc_services: ProcessorServices,
    sync_knowledge_file: KnowledgeDB,
):
    async def _parse_file_mock(
        qfile: QuivrFile,
        **processor_kwargs: dict[str, Any],
    ) -> list[Document]:
        with open(qfile.path, "rb") as f:
            return [Document(page_content=str(f.read()), metadata={})]

    km_processor = KnowledgeProcessor(proc_services)
    monkeypatch.setattr("quivr_worker.process.processor.parse_qfile", _parse_file_mock)
    km_dto = await sync_knowledge_file.to_dto(get_children=False, get_parent=False)
    await km_processor.process_knowledge(km_dto)

    # Check knowledge set to processed
    assert km_dto.id
    assert km_dto.brains
    knowledge_service = km_processor.services.knowledge_service
    km = await knowledge_service.get_knowledge(km_dto.id)
    assert km.status == KnowledgeStatus.PROCESSED
    assert km.brains[0].brain_id == km_dto.brains[0]["brain_id"]

    # Check vectors where added
    vecs = list(
        (
            await session.exec(
                select(Vector).where(col(Vector.knowledge_id) == km_dto.id)
            )
        ).all()
    )
    assert len(vecs) > 0
    assert vecs[0].metadata_ is not None


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("proc_services", [4], indirect=True)
async def test_process_sync_folder(
    monkeypatch,
    session: AsyncSession,
    proc_services: ProcessorServices,
    sync_knowledge_folder: KnowledgeDB,
):
    async def _parse_file_mock(
        qfile: QuivrFile,
        **processor_kwargs: dict[str, Any],
    ) -> list[Document]:
        with open(qfile.path, "rb") as f:
            return [Document(page_content=str(f.read()), metadata={})]

    km_processor = KnowledgeProcessor(proc_services)
    monkeypatch.setattr("quivr_worker.process.processor.parse_qfile", _parse_file_mock)
    km_dto = await sync_knowledge_folder.to_dto(get_children=False, get_parent=False)
    await km_processor.process_knowledge(km_dto)

    # Check knowledge set to processed
    assert km_dto.id
    assert km_dto.brains
    assert km_dto.brains[0]
    knowledge_service = km_processor.services.knowledge_service
    # FIXME (@AmineDiro): brain dto!!
    kms = await knowledge_service.get_all_knowledge_in_brain(
        km_dto.brains[0]["brain_id"]
    )

    # NOTE : this knowledge + 2 remote sync files
    assert len(kms) == 5
    for km in kms:
        assert km.status == KnowledgeStatus.PROCESSED
        assert km.brains[0]["brain_id"]
        assert km.brains[0]["brain_id"] == km_dto.brains[0]["brain_id"]

    # Check vectors where added
    vecs = list((await session.exec(select(Vector))).all())
    # Fake sync  return a folder half the time, we skip folders
    assert len(vecs) >= 2
    assert vecs[0].metadata_ is not None


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("proc_services", [1], indirect=True)
async def test_process_sync_folder_with_file_in_brain(
    monkeypatch,
    session: AsyncSession,
    proc_services: ProcessorServices,
    sync_knowledge_folder_with_file_in_brain: KnowledgeDB,
):
    async def _parse_file_mock(
        qfile: QuivrFile,
        **processor_kwargs: dict[str, Any],
    ) -> list[Document]:
        with open(qfile.path, "rb") as f:
            return [Document(page_content=str(f.read()), metadata={})]

    km_processor = KnowledgeProcessor(proc_services)
    monkeypatch.setattr("quivr_worker.process.processor.parse_qfile", _parse_file_mock)
    km_dto = await sync_knowledge_folder_with_file_in_brain.to_dto(
        get_children=False, get_parent=False
    )
    await km_processor.process_knowledge(km_dto)

    # Check knowledge set to processed
    assert km_dto.id
    assert km_dto.brains
    assert km_dto.brains[0]
    knowledge_service = km_processor.services.knowledge_service
    # FIXME (@AmineDiro): brain dto!!
    kms = await knowledge_service.get_all_knowledge_in_brain(
        km_dto.brains[0]["brain_id"]
    )

    # NOTE : this knowledge + 2 remote sync files
    assert len(kms) == 2
    for km in kms:
        assert km.status == KnowledgeStatus.PROCESSED
        assert len(km.brains) == 1, "File added to the same brain multiple times"
        assert km.brains[0]["brain_id"]
        assert km.brains[0]["brain_id"] == km_dto.brains[0]["brain_id"]

    # Check vectors
    vecs = list((await session.exec(select(Vector))).all())
    assert len(vecs) == 0, "File reprocessed, or folder processed "
