import os
from typing import AsyncGenerator, Callable, Type, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_core.api.repositories.base_repository import BaseRepository
from quivr_core.api.services.base_service import BaseService
from quivr_core.models.settings import settings
from quivr_core.storage.local_storage import LocalStorage
from quivr_core.storage.storage_base import StorageBase

R = TypeVar("R", bound=BaseRepository)
S = TypeVar("S", bound=BaseService)

async_engine = create_async_engine(
    settings.pg_database_async_url,
    echo=True if os.getenv("ORM_DEBUG") else False,
    future=True,
)

# TODO: get env variable and set it
storage = LocalStorage()


def get_storage() -> StorageBase:
    return storage


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session


def get_repository(repository_model: Type[R]) -> Callable[..., R]:
    def _get_repository(session: AsyncSession = Depends(get_async_session)) -> R:
        return repository_model(session)

    return _get_repository


def get_service(service: Type[S]) -> Callable[..., S]:
    def _get_service(
        repository: BaseRepository = Depends(
            get_repository(service.get_repository_cls())
        ),
    ) -> S:
        return service(repository)

    return _get_service
