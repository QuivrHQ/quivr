from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from backend.models.settings import settings

# TODO(@aminediro ): echo as param based on env
async_engine = create_async_engine(settings.pg_database_url, echo=True, future=True)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(async_engine) as session:
        yield session


def get_repository(repository):
    def _get_repository(session: AsyncSession = Depends(get_async_session)):
        return repository(session)

    return _get_repository
