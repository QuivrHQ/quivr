import os
from datetime import datetime, timedelta, timezone
from io import BytesIO
from typing import Any, Dict, List, Union

import pytest
from langchain_core.documents import Document
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.modules.sync.dto.outputs import SyncProvider
from quivr_api.modules.sync.entity.sync_models import SyncFile
from quivr_api.modules.sync.tests.test_sync_controller import FakeSync
from quivr_api.modules.sync.utils.sync import BaseSync
from quivr_api.modules.vector.entity.vector import Vector
from quivr_core.files.file import QuivrFile
from quivr_core.models import KnowledgeStatus
from quivr_worker.process.processor import KnowledgeProcessor, ProcessorServices
from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession


async def _parse_file_mock(
    qfile: QuivrFile,
    **processor_kwargs: dict[str, Any],
) -> list[Document]:
    with open(qfile.path, "rb") as f:
        return [Document(page_content=str(f.read()), metadata={})]


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("proc_services", [0], indirect=True)
async def test_refresh_sync_file(
    monkeypatch,
    session: AsyncSession,
    proc_services: ProcessorServices,
    sync_knowledge_file: KnowledgeDB,
):
    input_km = sync_knowledge_file
    assert input_km.id
    assert input_km.brains
    assert input_km.sync_file_id
    assert input_km.file_name
    assert input_km.source_link
    assert input_km.last_synced_at

    km_processor = KnowledgeProcessor(proc_services)
    monkeypatch.setattr("quivr_worker.process.processor.parse_qfile", _parse_file_mock)
    new_sync_file = SyncFile(
        id=input_km.sync_file_id,
        name=input_km.file_name,
        extension=input_km.extension,
        is_folder=False,
        web_view_link=input_km.source_link,
        last_modified_at=datetime.now(timezone.utc) - timedelta(hours=1),
    )
    sync_provider = FakeSync(provider_name=input_km.source, n_get_files=0)
    new_km = await km_processor.refresh_knowledge_entry(
        old_km=sync_knowledge_file,
        new_sync_file=new_sync_file,
        sync_provider=sync_provider,
        sync_credentials={},
    )

    # Check knowledge was updated
    assert new_km
    assert new_km.id
    knowledge_service = km_processor.services.knowledge_service
    km = await knowledge_service.get_knowledge(new_km.id)
    assert km.status == KnowledgeStatus.PROCESSED
    assert {b.brain_id for b in km.brains} == {b.brain_id for b in input_km.brains}
    assert km.parent_id == input_km.parent_id
    assert km.file_sha1 is not None
    assert km.last_synced_at
    assert km.last_synced_at > input_km.last_synced_at

    # Check vectors where removed
    vecs = list(
        (
            await session.exec(
                select(Vector).where(col(Vector.knowledge_id) == input_km.id)
            )
        ).all()
    )
    assert len(vecs) == 0

    # Check vectors where added for the new km
    vecs = list(
        (
            await session.exec(select(Vector).where(col(Vector.knowledge_id) == km.id))
        ).all()
    )
    assert len(vecs) > 0
    assert vecs[0].metadata_ is not None


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("proc_services", [0], indirect=True)
async def test_refresh_sync_file_rollback(
    monkeypatch,
    session: AsyncSession,
    proc_services: ProcessorServices,
    sync_knowledge_file_processed: KnowledgeDB,
):
    input_km = sync_knowledge_file_processed
    assert input_km.id
    assert input_km.brains
    assert input_km.sync_file_id
    assert input_km.file_name
    assert input_km.source_link
    assert input_km.last_synced_at

    async def _parse_file_mock_error(
        qfile: QuivrFile,
        **processor_kwargs: dict[str, Any],
    ) -> list[Document]:
        raise Exception("error")

    km_processor = KnowledgeProcessor(proc_services)
    monkeypatch.setattr(
        "quivr_worker.process.processor.parse_qfile", _parse_file_mock_error
    )
    new_sync_file = SyncFile(
        id=input_km.sync_file_id,
        name=input_km.file_name,
        extension=input_km.extension,
        is_folder=False,
        web_view_link=input_km.source_link,
        last_modified_at=datetime.now(timezone.utc) - timedelta(hours=1),
    )
    sync_provider = FakeSync(provider_name=input_km.source, n_get_files=0)
    new_km = await km_processor.refresh_knowledge_entry(
        old_km=input_km,
        new_sync_file=new_sync_file,
        sync_provider=sync_provider,
        sync_credentials={},
    )

    # Check knowledge was not removed
    assert new_km is None

    # Check vectors where not removed
    vecs = list(
        (
            await session.exec(
                select(Vector).where(col(Vector.knowledge_id) == input_km.id)
            )
        ).all()
    )
    # Check nothing was added
    assert len(vecs) == 1

    # Check kms statyed correct
    all_kms = list((await session.exec(select(KnowledgeDB))).unique().all())
    assert len(all_kms) == 1
    assert all_kms[0].id == input_km.id
    assert all_kms[0].last_synced_at == input_km.last_synced_at


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("proc_services", [2], indirect=True)
async def test_refresh_sync_folder(
    monkeypatch,
    session: AsyncSession,
    proc_services: ProcessorServices,
    sync_knowledge_folder_processed: KnowledgeDB,
):
    input_km_folder = sync_knowledge_folder_processed
    assert input_km_folder.id
    assert input_km_folder.brains
    assert input_km_folder.sync_file_id
    assert input_km_folder.file_name
    assert input_km_folder.source_link
    assert input_km_folder.last_synced_at

    class _MockSync:
        name = "FakeProvider"
        lower_name = "google"
        datetime_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"

        async def aget_files(
            self, credentials: Dict, file_ids: List[str]
        ) -> List[SyncFile]:
            return self.get_files(credentials, file_ids)

        def get_files(self, credentials: Dict, file_ids: List[str]) -> List[SyncFile]:
            return [
                SyncFile(
                    id="file_id_1",
                    name="new_file",
                    extension=".txt",
                    web_view_link="fake://test.com",
                    is_folder=False,
                    last_modified_at=datetime.now(),
                )
            ]

        async def adownload_file(
            self, credentials: Dict, file: SyncFile
        ) -> Dict[str, Union[str, BytesIO]]:
            return {"content": str(os.urandom(24))}

    sync_provider_mapping: dict[SyncProvider, BaseSync] = {
        provider: _MockSync()  # type: ignore
        for provider in list(SyncProvider)
    }

    input_km_children = await input_km_folder.awaitable_attrs.children
    proc_services.syncprovider_mapping = sync_provider_mapping
    km_processor = KnowledgeProcessor(proc_services)
    monkeypatch.setattr("quivr_worker.process.processor.parse_qfile", _parse_file_mock)
    await km_processor.refresh_sync_folder(folder_km=input_km_folder)

    # Check knowledge was updated
    assert input_km_folder
    assert input_km_folder.id
    knowledge_service = km_processor.services.knowledge_service
    km = await knowledge_service.get_knowledge(input_km_folder.id)
    assert km.status == KnowledgeStatus.PROCESSED
    assert {k.id for k in await km.awaitable_attrs.children}.issuperset(
        {k.id for k in input_km_children}
    )
