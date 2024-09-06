from datetime import datetime
from uuid import UUID

from notion_client import Client
from quivr_api.logger import get_logger
from quivr_api.modules.sync.repository.sync_repository import NotionRepository
from quivr_api.modules.sync.service.sync_notion import (
    SyncNotionService,
    fetch_limit_notion_pages,
    store_notion_pages,
)
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import text
from sqlmodel.ext.asyncio.session import AsyncSession

logger = get_logger("celery_worker")


async def fetch_and_store_notion_files_async(
    async_engine: AsyncEngine, access_token: str, user_id: UUID
):
    try:
        async with AsyncSession(
            async_engine, expire_on_commit=False, autoflush=False
        ) as session:
            await session.execute(
                text("SET SESSION idle_in_transaction_session_timeout = '5min';")
            )
            notion_repository = NotionRepository(session)
            notion_service = SyncNotionService(notion_repository)
            notion_client = Client(auth=access_token)
            all_search_result = fetch_limit_notion_pages(
                notion_client,
                last_sync_time=datetime(1970, 1, 1, 0, 0, 0),  # UNIX EPOCH
            )
            logger.debug(f"Notion fetched {len(all_search_result)} pages")
            pages = await store_notion_pages(all_search_result, notion_service, user_id)
            if pages:
                logger.info(f"stored {len(pages)} from notion for {user_id}")
            else:
                logger.warn("No notion page fetched")

    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()
