import time
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
from io import BytesIO
from typing import Any, AsyncGenerator, Generator, List, Tuple
from uuid import UUID

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import get_supabase_async_client
from quivr_api.modules.knowledge.dto.inputs import AddKnowledge
from quivr_api.modules.knowledge.dto.outputs import KnowledgeDTO
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB, KnowledgeSource
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.repository.storage import SupabaseS3Storage
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.sync.dto.outputs import SyncProvider
from quivr_api.modules.sync.entity.sync_models import SyncFile
from quivr_api.modules.sync.repository.sync_repository import SyncsRepository
from quivr_api.modules.sync.service.sync_service import SyncsService
from quivr_api.modules.sync.utils.sync import (
    AzureDriveSync,
    BaseSync,
    DropboxSync,
    GitHubSync,
    GoogleDriveSync,
)
from quivr_api.modules.vector.repository.vectors_repository import VectorRepository
from quivr_api.modules.vector.service.vector_service import VectorService
from quivr_core.files.file import FileExtension, QuivrFile
from quivr_core.models import KnowledgeStatus
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_worker.files import build_file, compute_sha1

logger = get_logger("celery_worker")


def skip_process(knowledge: KnowledgeDTO) -> bool:
    return knowledge.is_folder and knowledge.source != KnowledgeSource.NOTION


def build_syncprovider_mapping() -> dict[str, BaseSync]:
    mapping_sync_utils = {
        "google": GoogleDriveSync(),
        "azure": AzureDriveSync(),
        "dropbox": DropboxSync(),
        "github": GitHubSync(),
        # "notion", NotionSync(notion_service=notion_service),
    }
    return mapping_sync_utils


@dataclass
class ProcessorServices:
    sync_service: SyncsService
    vector_service: VectorService
    knowledge_service: KnowledgeService
    syncprovider_mapping: dict[str, BaseSync]


@asynccontextmanager
async def _start_session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        try:
            await session.execute(
                text("SET SESSION idle_in_transaction_session_timeout = '5min';")
            )
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


@asynccontextmanager
async def build_processor_services(engine: AsyncEngine):
    async_client = await get_supabase_async_client()
    storage = SupabaseS3Storage(async_client)
    try:
        async with _start_session(engine) as async_session:
            vector_repository = VectorRepository(async_session.sync_session)
            vector_service = VectorService(vector_repository)
            knowledge_repository = KnowledgeRepository(async_session)
            knowledge_service = KnowledgeService(knowledge_repository, storage=storage)
            sync_repository = SyncsRepository(async_session)
            sync_service = SyncsService(sync_repository)
            yield ProcessorServices(
                knowledge_service=knowledge_service,
                vector_service=vector_service,
                sync_service=sync_service,
                syncprovider_mapping=build_syncprovider_mapping(),
            )
    finally:
        logger.info("Closing processor services")


async def download_sync_file(
    sync_provider: BaseSync, file: SyncFile, credentials: dict[str, Any]
) -> bytes:
    logger.info(f"Downloading {file} using {sync_provider}")
    file_response = await sync_provider.adownload_file(credentials, file)
    logger.debug(f"Fetch sync file response: {file_response}")
    raw_data = file_response["content"]
    if isinstance(raw_data, BytesIO):
        file_data = raw_data.read()
    else:
        file_data = raw_data.encode("utf-8")
    logger.debug(f"Successfully downloaded sync file : {file}")
    return file_data


@contextmanager
def build_qfile(
    knowledge: KnowledgeDB, file_data: bytes
) -> Generator[QuivrFile, None, None]:
    assert knowledge.id
    assert knowledge.file_name
    assert knowledge.file_sha1
    with build_file(
        file_data=file_data, file_name_ext=knowledge.file_name
    ) as tmp_file_path:
        qfile = QuivrFile(
            id=knowledge.id,
            original_filename=knowledge.file_name,
            path=tmp_file_path,
            file_sha1=knowledge.file_sha1,
            file_extension=FileExtension(knowledge.extension),
            file_size=knowledge.file_size,
            metadata={
                "date": time.strftime("%Y%m%d"),
                "file_name": knowledge.file_name,
                "knowledge_id": knowledge.id,
            },
        )
        if knowledge.metadata_:
            qfile.additional_metadata = {
                **qfile.metadata,
                **knowledge.metadata_,
            }
        yield qfile


class KnowledgeProcessor:
    def __init__(self, services: ProcessorServices):
        self.services = services

    async def fetch_sync_knowledge(
        self,
        sync_id: int,
        user_id: UUID,
        folder_id: str | None,
    ) -> Tuple[dict[str, KnowledgeDB], List[SyncFile] | None]:
        map_knowledges_task = self.services.knowledge_service.map_syncs_knowledge_user(
            sync_id=sync_id, user_id=user_id
        )
        sync_files_task = self.services.sync_service.get_files_folder_user_sync(
            sync_id,
            user_id,
            folder_id,
        )
        return await asyncio.gather(*[map_knowledges_task, sync_files_task])  # type: ignore  # noqa: F821

    @asynccontextmanager
    async def build_processable(
        self, knowledge: KnowledgeDTO
    ) -> AsyncGenerator[Tuple[KnowledgeDB, QuivrFile] | None, None]:
        if knowledge.source == KnowledgeSource.LOCAL:
            async with self._build_local(knowledge) as to_process:
                yield to_process
        elif knowledge.source in (
            KnowledgeSource.AZURE,
            KnowledgeSource.GITHUB,
            KnowledgeSource.GOOGLE,
            KnowledgeSource.NOTION,
        ):
            async with self._build_sync(knowledge) as to_process:
                yield to_process
        elif knowledge.source == KnowledgeSource.WEB:
            raise NotImplementedError
        else:
            logger.error(
                f"received knowledge : {knowledge.id} with unknown source: {knowledge.source}"
            )
            raise ValueError("Unknown knowledge source : {knoledge.source}")

    @asynccontextmanager
    async def _build_local(
        self, knowledge: KnowledgeDTO
    ) -> AsyncGenerator[Tuple[KnowledgeDB, QuivrFile] | None, None]:
        if knowledge.id is None or knowledge.file_name is None:
            logger.error(f"received unprocessable local knowledge : {knowledge.id} ")
            raise ValueError(
                f"received unprocessable local knowledge : {knowledge.id} "
            )
        knowledge_db = await self.services.knowledge_service.get_knowledge(knowledge.id)
        file_data = await self.services.knowledge_service.storage.download_file(
            knowledge_db
        )
        knowledge_db.file_sha1 = compute_sha1(file_data)
        with build_qfile(knowledge_db, file_data) as qfile:
            yield (knowledge_db, qfile)

    @asynccontextmanager
    async def _build_sync(
        self, knowledge_dto: KnowledgeDTO
    ) -> AsyncGenerator[Tuple[KnowledgeDB, QuivrFile] | None, None]:
        if knowledge_dto.id is None:
            logger.error(f"received unprocessable knowledge: {knowledge_dto.id} ")
            raise ValueError

        parent_knowledge = await self.services.knowledge_service.get_knowledge(
            knowledge_dto.id
        )
        if parent_knowledge.file_name is None:
            logger.error(f"received unprocessable knowledge : {parent_knowledge.id} ")
            raise ValueError(
                f"received unprocessable knowledge : {parent_knowledge.id} "
            )
        if (
            parent_knowledge.sync_file_id is None
            or parent_knowledge.sync_id is None
            or parent_knowledge.source_link is None
        ):
            logger.error(
                f"unprocessable  sync knowledge : {parent_knowledge.id}. no sync_file_id"
            )
            raise ValueError(
                f"received unprocessable knowledge : {parent_knowledge.id} "
            )
        # Get associated sync
        sync = await self.services.sync_service.get_sync_by_id(parent_knowledge.sync_id)
        if sync.credentials is None:
            logger.error(f"can't process sync file. sync {sync.id} has no credentials")
            return
        provider_name = SyncProvider(sync.provider.lower())
        sync_provider = self.services.syncprovider_mapping[provider_name]

        syncfile_to_knowledge, sync_files = await self.fetch_sync_knowledge(
            sync_id=parent_knowledge.sync_id,
            user_id=parent_knowledge.user_id,
            folder_id=parent_knowledge.sync_file_id,
        )
        if not sync_files:
            return

        # Yield parent knowledge to process
        file_data = await download_sync_file(
            sync_provider=sync_provider,
            file=SyncFile(
                id=parent_knowledge.sync_file_id,
                name=parent_knowledge.file_name,
                extension=parent_knowledge.extension,
                web_view_link=parent_knowledge.source_link,
                is_folder=parent_knowledge.is_folder,
                last_modified_at=parent_knowledge.updated_at,
            ),
            credentials=sync.credentials,
        )
        parent_knowledge.file_sha1 = compute_sha1(file_data)
        with build_qfile(parent_knowledge, file_data) as qfile:
            yield (parent_knowledge, qfile)

        for sync_file in sync_files:
            existing_km = syncfile_to_knowledge.get(sync_file.id)
            if existing_km:
                file_knowledge = existing_km
            else:
                # create sync file knowledge
                # automagically gets the brains associated with the parent
                file_knowledge = await self.services.knowledge_service.create_knowledge(
                    user_id=parent_knowledge.user_id,
                    knowledge_to_add=AddKnowledge(
                        file_name=sync_file.name,
                        is_folder=sync_file.is_folder,
                        extension=sync_file.extension,
                        source=parent_knowledge.source,  # same as parent
                        source_link=sync_file.web_view_link,
                        parent_id=parent_knowledge.id,
                        sync_id=parent_knowledge.sync_id,
                        sync_file_id=sync_file.id,
                    ),
                    status=KnowledgeStatus.PROCESSING,
                    upload_file=None,
                )
            file_data = await download_sync_file(
                sync_provider=sync_provider,
                file=sync_file,
                credentials=sync.credentials,
            )
            file_knowledge.file_sha1 = compute_sha1(file_data)
            with build_qfile(file_knowledge, file_data) as qfile:
                yield (file_knowledge, qfile)

    async def process_knowledge(self, knowledge_dto: KnowledgeDTO):
        async for (knowledge, qfile) in self.build_processable(knowledge_dto):
            pass
