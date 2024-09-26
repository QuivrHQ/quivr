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
    proc_services: ProcessorServices,
    local_knowledge_file: KnowledgeDB,
):
    input_km = local_knowledge_file

    async def _parse_file_mock(
        qfile: QuivrFile,
        **processor_kwargs: dict[str, Any],
    ) -> list[Document]:
        with open(qfile.path, "rb") as f:
            return [Document(page_content=str(f.read()), metadata={})]

    monkeypatch.setattr("quivr_worker.process.processor.parse_qfile", _parse_file_mock)
    assert input_km.id
    assert input_km.brains
    km_processor = KnowledgeProcessor(proc_services)
    await km_processor.process_knowledge(input_km.id)

    # Check knowledge processed
    knowledge_service = km_processor.services.knowledge_service
    km = await knowledge_service.get_knowledge(input_km.id)
    assert km.status == KnowledgeStatus.PROCESSED
    assert km.brains[0].brain_id == input_km.brains[0].brain_id
    assert km.file_sha1 is not None

    # Check vectors where added
    vecs = list(
        (
            await session.exec(
                select(Vector).where(col(Vector.knowledge_id) == input_km.id)
            )
        ).all()
    )
    assert len(vecs) > 0
    assert vecs[0].metadata_ is not None


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("proc_services", [0], indirect=True)
async def test_process_web_file(
    monkeypatch,
    session: AsyncSession,
    proc_services: ProcessorServices,
    web_knowledge: KnowledgeDB,
):
    input_km = web_knowledge

    async def _extract_url(url: str) -> str:
        return "quivr has the best rag"

    async def _parse_file_mock(
        qfile: QuivrFile,
        **processor_kwargs: dict[str, Any],
    ) -> list[Document]:
        with open(qfile.path, "rb") as f:
            return [Document(page_content=str(f.read()), metadata={})]

    monkeypatch.setattr("quivr_worker.process.processor.parse_qfile", _parse_file_mock)
    monkeypatch.setattr("quivr_worker.process.processor.extract_from_url", _extract_url)
    assert input_km.id
    assert input_km.brains
    km_processor = KnowledgeProcessor(proc_services)
    await km_processor.process_knowledge(input_km.id)

    # Check knowledge processed
    knowledge_service = km_processor.services.knowledge_service
    km = await knowledge_service.get_knowledge(input_km.id)
    assert km.status == KnowledgeStatus.PROCESSED
    assert km.brains[0].brain_id == input_km.brains[0].brain_id
    assert km.file_sha1 is not None

    # Check vectors where added
    vecs = list(
        (
            await session.exec(
                select(Vector).where(col(Vector.knowledge_id) == input_km.id)
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
    input_km = sync_knowledge_file
    assert input_km.id
    assert input_km.brains

    async def _parse_file_mock(
        qfile: QuivrFile,
        **processor_kwargs: dict[str, Any],
    ) -> list[Document]:
        with open(qfile.path, "rb") as f:
            return [Document(page_content=str(f.read()), metadata={})]

    km_processor = KnowledgeProcessor(proc_services)
    monkeypatch.setattr("quivr_worker.process.processor.parse_qfile", _parse_file_mock)
    await km_processor.process_knowledge(input_km.id)

    # Check knowledge set to processed
    knowledge_service = km_processor.services.knowledge_service
    km = await knowledge_service.get_knowledge(input_km.id)
    assert km.status == KnowledgeStatus.PROCESSED
    assert km.brains[0].brain_id == input_km.brains[0].brain_id
    assert km.file_sha1 is not None

    # Check vectors where added
    vecs = list(
        (
            await session.exec(
                select(Vector).where(col(Vector.knowledge_id) == input_km.id)
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
    input_km = sync_knowledge_folder
    assert input_km.id
    assert input_km.brains

    async def _parse_file_mock(
        qfile: QuivrFile,
        **processor_kwargs: dict[str, Any],
    ) -> list[Document]:
        with open(qfile.path, "rb") as f:
            return [Document(page_content=str(f.read()), metadata={})]

    km_processor = KnowledgeProcessor(proc_services)
    monkeypatch.setattr("quivr_worker.process.processor.parse_qfile", _parse_file_mock)
    await km_processor.process_knowledge(input_km.id)

    # Check knowledge set to processed
    assert input_km.id
    assert input_km.brains
    assert input_km.brains[0]
    knowledge_service = km_processor.services.knowledge_service
    # FIXME (@AmineDiro): brain dto!!
    kms = await knowledge_service.get_all_knowledge_in_brain(
        input_km.brains[0].brain_id
    )

    # NOTE : this knowledge + 2 remote sync files
    assert len(kms) == 5
    for km in kms:
        assert km.status == KnowledgeStatus.PROCESSED
        assert km.brains[0]["brain_id"]
        assert km.brains[0]["brain_id"] == input_km.brains[0].brain_id
        assert km.file_sha1 is not None

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
    input_km = sync_knowledge_folder_with_file_in_brain
    assert input_km.id
    assert input_km.brains

    async def _parse_file_mock(
        qfile: QuivrFile,
        **processor_kwargs: dict[str, Any],
    ) -> list[Document]:
        with open(qfile.path, "rb") as f:
            return [Document(page_content=str(f.read()), metadata={})]

    km_processor = KnowledgeProcessor(proc_services)
    monkeypatch.setattr("quivr_worker.process.processor.parse_qfile", _parse_file_mock)
    await km_processor.process_knowledge(input_km.id)

    # Check knowledge set to processed
    assert input_km.id
    assert input_km.brains
    assert input_km.brains[0]
    knowledge_service = km_processor.services.knowledge_service
    # FIXME (@AmineDiro): brain dto!!
    kms = await knowledge_service.get_all_knowledge_in_brain(
        input_km.brains[0].brain_id
    )

    # NOTE : this knowledge + 2 remote sync files
    assert len(kms) == 2
    for km in kms:
        assert km.status == KnowledgeStatus.PROCESSED
        assert len(km.brains) == 1, "File added to the same brain multiple times"
        assert km.brains[0]["brain_id"]
        assert km.brains[0]["brain_id"] == input_km.brains[0].brain_id

    # Check vectors
    vecs = list((await session.exec(select(Vector))).all())
    assert len(vecs) == 0, "File reprocessed, or folder processed "


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("proc_services", [1], indirect=True)
async def test_process_sync_folder_with_file_in_other_brain(
    monkeypatch,
    session: AsyncSession,
    proc_services: ProcessorServices,
    sync_knowledge_folder_with_file_in_other_brain: KnowledgeDB,
):
    input_km = sync_knowledge_folder_with_file_in_other_brain
    assert input_km.id
    assert input_km.brains

    async def _parse_file_mock(
        qfile: QuivrFile,
        **processor_kwargs: dict[str, Any],
    ) -> list[Document]:
        with open(qfile.path, "rb") as f:
            return [Document(page_content=str(f.read()), metadata={})]

    km_processor = KnowledgeProcessor(proc_services)
    monkeypatch.setattr("quivr_worker.process.processor.parse_qfile", _parse_file_mock)
    await km_processor.process_knowledge(input_km.id)

    # Check knowledge set to processed
    assert input_km.id
    assert input_km.brains
    assert input_km.brains[0]
    knowledge_service = km_processor.services.knowledge_service
    # FIXME (@AmineDiro): brain dto!!
    kms = await knowledge_service.get_all_knowledge_in_brain(
        input_km.brains[0].brain_id
    )

    assert len(kms) == 2
    for km in kms:
        assert km.status == KnowledgeStatus.PROCESSED
        assert len(km.brains) >= 1, "File added to the same brain multiple times"
        assert km.brains[0]["brain_id"]
        assert input_km.brains[0].brain_id in {b["brain_id"] for b in km.brains}
        if len(km.brains) > 1:
            assert len({b["brain_id"] for b in km.brains}) == 2

    # Check vectors
    vecs = list((await session.exec(select(Vector))).all())
    assert len(vecs) == 0, "File reprocessed, or folder processed "


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("proc_services", [0], indirect=True)
async def test_process_km_rollback(
    monkeypatch,
    session: AsyncSession,
    proc_services: ProcessorServices,
    local_knowledge_file: KnowledgeDB,
):
    input_km = local_knowledge_file
    assert input_km.id
    assert input_km.brains

    async def _parse_file_mock(
        qfile: QuivrFile,
        **processor_kwargs: dict[str, Any],
    ) -> list[Document]:
        with open(qfile.path, "rb") as f:
            return [Document(page_content=str(f.read()), metadata={})]

    async def _update_km_error(*args, **kwargs):
        raise Exception("Error")

    monkeypatch.setattr("quivr_worker.process.processor.parse_qfile", _parse_file_mock)

    km_processor = KnowledgeProcessor(proc_services)

    # Set error at the end
    km_processor.services.knowledge_service.update_knowledge = _update_km_error

    await km_processor.process_knowledge(input_km.id)

    # Check knowledge set to processed
    knowledge_service = km_processor.services.knowledge_service
    km = await knowledge_service.get_knowledge(input_km.id)
    assert km.status == KnowledgeStatus.PROCESSING  # tests are just uploaded
    vecs = list((await session.exec(select(Vector))).all())
    # Check we remove the vectors
    assert len(vecs) == 0
