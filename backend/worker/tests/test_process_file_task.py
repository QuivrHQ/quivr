from typing import Any

import pytest
from langchain_core.documents import Document
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.modules.vector.entity.vector import Vector
from quivr_core.files.file import QuivrFile
from quivr_core.models import KnowledgeStatus
from quivr_worker.process.processor import KnowledgeProcessor
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.mark.asyncio(loop_scope="session")
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
