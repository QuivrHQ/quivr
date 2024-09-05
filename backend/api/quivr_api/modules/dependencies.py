import os
from typing import AsyncGenerator, Callable, Generator, Generic, Optional, Type, TypeVar

from fastapi import Depends
from langchain.embeddings.base import Embeddings
from langchain_community.embeddings.ollama import OllamaEmbeddings

# from langchain_community.vectorstores.supabase import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings

# from quivr_api.modules.vector.service.vector_service import VectorService
# from quivr_api.modules.vectorstore.supabase import CustomSupabaseVectorStore
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.logger import get_logger
from quivr_api.models.databases.supabase.supabase import SupabaseDB
from quivr_api.models.settings import BrainSettings
from supabase.client import AsyncClient, Client, create_async_client, create_client

# Global variables to store the Supabase client and database instances
_supabase_client: Optional[Client] = None
_supabase_async_client: Optional[AsyncClient] = None
_supabase_db: Optional[SupabaseDB] = None
_db_engine: Optional[Engine] = None
_embedding_service = None

settings = BrainSettings()  # type: ignore

logger = get_logger(__name__)


class BaseRepository:
    def __init__(self, session: AsyncSession | Session):
        self.session = session


R = TypeVar("R", bound=BaseRepository)


class BaseService(Generic[R]):
    # associated repository type
    repository_cls: Type[R]

    def __init__(self, repository: R):
        self.repository = repository

    @classmethod
    def get_repository_cls(cls) -> Type[R]:
        return cls.repository_cls  # type: ignore


S = TypeVar("S", bound=BaseService)

sync_engine = create_engine(
    settings.pg_database_url,
    echo=True if os.getenv("ORM_DEBUG") else False,
    future=True,
    # NOTE: pessimistic bound on
    pool_pre_ping=True,
    pool_size=10,  # NOTE: no bouncer for now, if 6 process workers => 6
    pool_recycle=1800,
)
async_engine = create_async_engine(
    settings.pg_database_async_url,
    connect_args={"server_settings": {"application_name": "quivr-api-async"}},
    echo=True if os.getenv("ORM_DEBUG") else False,
    future=True,
    pool_pre_ping=True,
    pool_size=5,  # NOTE: no bouncer for now, if 6 process workers => 6
    pool_recycle=1800,
    isolation_level="AUTOCOMMIT",
)


def get_sync_session() -> Generator[Session, None, None]:
    with Session(sync_engine, expire_on_commit=False, autoflush=False) as session:
        yield session


# def get_documents_vector_store(vector_service: VectorService) -> SupabaseVectorStore:
#     embeddings = get_embedding_client()
#     supabase_client: Client = get_supabase_client()
#     documents_vector_store = CustomSupabaseVectorStore(  # Modified by @chloe Check
#         supabase_client, embeddings, table_name="vectors", vector_service=vector_service
#     )
#     return documents_vector_store


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(
        async_engine,
    ) as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()


def get_repository(repository_model: Type[R], asynchronous=True) -> Callable[..., R]:
    def _get_repository(session: AsyncSession = Depends(get_async_session)) -> R:
        return repository_model(session)

    def _get_sync_repository(session: Session = Depends(get_sync_session)) -> R:
        return repository_model(session)

    if asynchronous:
        return _get_repository
    return _get_sync_repository


def get_embedding_client() -> Embeddings:
    global _embedding_service
    if settings.ollama_api_base_url:
        embeddings = OllamaEmbeddings(
            base_url=settings.ollama_api_base_url,
        )  # pyright: ignore reportPrivateUsage=none
    else:
        embeddings = OpenAIEmbeddings()  # pyright: ignore reportPrivateUsage=none
    return embeddings


def get_pg_database_engine():
    global _db_engine
    if _db_engine is None:
        logger.info("Creating Postgres DB engine")
        _db_engine = create_engine(settings.pg_database_url, pool_pre_ping=True)
    return _db_engine


def get_pg_database_async_engine():
    global _db_engine
    if _db_engine is None:
        logger.info("Creating Postgres DB engine")
        _db_engine = create_engine(settings.pg_database_async_url, pool_pre_ping=True)
    return _db_engine


async def get_supabase_async_client() -> AsyncClient:
    global _supabase_async_client
    if _supabase_async_client is None:
        logger.info("Creating Supabase client")
        _supabase_async_client = await create_async_client(
            settings.supabase_url, settings.supabase_service_key
        )
    return _supabase_async_client


def get_supabase_client() -> Client:
    global _supabase_client
    if _supabase_client is None:
        logger.info("Creating Supabase client")
        _supabase_client = create_client(
            settings.supabase_url, settings.supabase_service_key
        )
    return _supabase_client


def get_supabase_db() -> SupabaseDB:
    global _supabase_db
    if _supabase_db is None:
        logger.info("Creating Supabase DB")
        _supabase_db = SupabaseDB(get_supabase_client())
    return _supabase_db


def get_service(service: Type[S], asynchronous=True) -> Callable[..., S]:
    def _get_service(
        repository: BaseRepository = Depends(
            get_repository(service.get_repository_cls(), asynchronous)  # type: ignore
        ),
    ) -> S:
        return service(repository)

    return _get_service
