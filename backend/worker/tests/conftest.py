import os
from io import BytesIO
from uuid import uuid4

import pytest
import pytest_asyncio
import sqlalchemy
from fastapi import UploadFile
from langchain_core.embeddings import DeterministicFakeEmbedding
from quivr_api.models.settings import settings
from quivr_api.modules.brain.entity.brain_entity import Brain, BrainType
from quivr_api.modules.brain.entity.brain_user import BrainUserDB
from quivr_api.modules.dependencies import get_supabase_client
from quivr_api.modules.knowledge.dto.inputs import AddKnowledge
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.knowledge.tests.conftest import FakeStorage
from quivr_api.modules.sync.dto.outputs import SyncProvider
from quivr_api.modules.sync.entity.sync_models import Sync
from quivr_api.modules.sync.repository.sync_repository import SyncsRepository
from quivr_api.modules.sync.service.sync_service import SyncsService
from quivr_api.modules.sync.tests.test_sync_controller import BaseFakeSync
from quivr_api.modules.sync.utils.sync import BaseSync
from quivr_api.modules.user.entity.user_identity import User
from quivr_api.modules.vector.repository.vectors_repository import VectorRepository
from quivr_api.modules.vector.service.vector_service import VectorService
from quivr_core.files.file import QuivrFile
from quivr_core.models import KnowledgeStatus
from quivr_worker.process.processor import KnowledgeProcessor, ProcessorServices
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

pg_database_base_url = "postgres:postgres@localhost:54322/postgres"


async_engine = create_async_engine(
    "postgresql+asyncpg://" + pg_database_base_url,
    echo=True if os.getenv("ORM_DEBUG") else False,
    future=True,
)


@pytest_asyncio.fixture(scope="function")
async def session():
    async with async_engine.connect() as conn:
        trans = await conn.begin()
        nested = await conn.begin_nested()
        async_session = AsyncSession(
            conn,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

        @sqlalchemy.event.listens_for(
            async_session.sync_session, "after_transaction_end"
        )
        def end_savepoint(session, transaction):
            nonlocal nested
            if not nested.is_active:
                nested = conn.sync_connection.begin_nested()  # type: ignore

        yield async_session
        await trans.rollback()
        await async_session.close()


@pytest.fixture(scope="session")
def supabase_client():
    return get_supabase_client()


@pytest_asyncio.fixture(scope="function")
async def user(session: AsyncSession) -> User:
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    assert user_1.id
    return user_1


@pytest_asyncio.fixture(scope="function")
async def brain_user(session, user: User) -> Brain:
    assert user.id
    brain_1 = Brain(
        name="test_brain",
        description="this is a test brain",
        brain_type=BrainType.integration,
    )
    session.add(brain_1)
    await session.commit()
    await session.refresh(brain_1)
    assert brain_1.brain_id
    brain_user = BrainUserDB(
        brain_id=brain_1.brain_id, user_id=user.id, default_brain=True, rights="Owner"
    )
    session.add(brain_user)
    await session.commit()
    return brain_1


# NOTE: param sets the number of sync file the provider returns
@pytest_asyncio.fixture(scope="function")
async def proc_services(session: AsyncSession, request) -> ProcessorServices:
    storage = FakeStorage()
    embedder = DeterministicFakeEmbedding(size=settings.embedding_dim)
    vector_repository = VectorRepository(session)
    vector_service = VectorService(vector_repository, embedder=embedder)
    knowledge_repository = KnowledgeRepository(session)
    knowledge_service = KnowledgeService(knowledge_repository, storage=storage)
    sync_provider_mapping: dict[SyncProvider, BaseSync] = {
        provider: BaseFakeSync(provider_name=str(provider), n_get_files=request.param)
        for provider in list(SyncProvider)
    }
    sync_repository = SyncsRepository(
        session, sync_provider_mapping=sync_provider_mapping
    )
    sync_service = SyncsService(sync_repository)

    return ProcessorServices(
        knowledge_service=knowledge_service,
        vector_service=vector_service,
        sync_service=sync_service,
        syncprovider_mapping=sync_provider_mapping,
    )


@pytest_asyncio.fixture(scope="function")
async def km_processor(proc_services: ProcessorServices):
    return KnowledgeProcessor(proc_services)


@pytest_asyncio.fixture(scope="function")
async def sync(session: AsyncSession, user: User) -> Sync:
    assert user.id
    sync = Sync(
        name="test_sync",
        email="test@test.com",
        user_id=user.id,
        credentials={"test": "test"},
        provider=SyncProvider.GOOGLE,
    )

    session.add(sync)
    await session.commit()
    await session.refresh(sync)
    return sync


@pytest_asyncio.fixture(scope="function")
async def local_knowledge_file(
    proc_services: ProcessorServices, user: User, brain_user: Brain
) -> KnowledgeDB:
    assert user.id
    assert brain_user.brain_id
    service = proc_services.knowledge_service
    km_to_add = AddKnowledge(
        file_name="test",
        source="local",
        is_folder=False,
        parent_id=None,
    )
    km_data = BytesIO(os.urandom(24))
    km = await service.create_knowledge(
        user_id=user.id,
        knowledge_to_add=km_to_add,
        upload_file=UploadFile(file=km_data, size=128, filename=km_to_add.file_name),
    )

    # Link it to the brain
    await service.link_knowledge_tree_brains(
        km, brains_ids=[brain_user.brain_id], user_id=user.id
    )
    return km


@pytest_asyncio.fixture(scope="function")
async def sync_knowledge_file(
    session: AsyncSession,
    proc_services: ProcessorServices,
    user: User,
    brain_user: Brain,
    sync: Sync,
) -> KnowledgeDB:
    assert user.id
    assert brain_user.brain_id

    km = KnowledgeDB(
        file_name="test_file_1.txt",
        extension=".txt",
        status=KnowledgeStatus.PROCESSING,
        source=SyncProvider.GOOGLE,
        source_link="drive://test/test",
        file_size=0,
        file_sha1=None,
        user_id=user.id,
        brains=[brain_user],
        parent=None,
        sync_file_id="id1",
        sync=sync,
    )

    session.add(km)
    await session.commit()
    await session.refresh(km)

    return km


@pytest_asyncio.fixture(scope="function")
async def sync_knowledge_folder(
    session: AsyncSession,
    proc_services: ProcessorServices,
    user: User,
    brain_user: Brain,
    sync: Sync,
) -> KnowledgeDB:
    assert user.id
    assert brain_user.brain_id

    km = KnowledgeDB(
        file_name="folder1",
        extension=".txt",
        status=KnowledgeStatus.PROCESSING,
        source=SyncProvider.GOOGLE,
        source_link="drive://test/folder1",
        file_size=0,
        file_sha1=None,
        user_id=user.id,
        brains=[brain_user],
        parent=None,
        is_folder=True,
        sync_file_id="id1",
        sync=sync,
    )

    session.add(km)
    await session.commit()
    await session.refresh(km)

    return km


@pytest.fixture
def qfile_instance(tmp_path) -> QuivrFile:
    data = "This is some test data."
    temp_file = tmp_path / "data.txt"
    temp_file.write_text(data)
    knowledge_id = uuid4()
    return QuivrFile(
        id=knowledge_id,
        file_sha1="124",
        file_extension=".txt",
        original_filename=temp_file.name,
        path=temp_file.absolute(),
        file_size=len(data),
    )


@pytest.fixture
def audio_file(tmp_path) -> QuivrFile:
    data = os.urandom(128)
    temp_file = tmp_path / "data.mp4"
    temp_file.write_bytes(data)
    knowledge_id = uuid4()
    return QuivrFile(
        id=knowledge_id,
        file_sha1="124",
        file_extension=".mp4",
        original_filename="data.mp4",
        path=temp_file.absolute(),
        file_size=len(data),
    )
