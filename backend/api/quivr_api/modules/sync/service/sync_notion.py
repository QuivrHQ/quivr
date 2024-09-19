from datetime import datetime, timezone
from typing import List, Sequence
from uuid import UUID

from notion_client import Client

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseService
from quivr_api.modules.sync.entity.notion_page import NotionPage, NotionSearchResult
from quivr_api.modules.sync.entity.sync_models import NotionSyncFile
from quivr_api.modules.sync.repository.sync_repository import NotionRepository

logger = get_logger(__name__)


class SyncNotionService(BaseService[NotionRepository]):
    repository_cls = NotionRepository

    def __init__(self, repository: NotionRepository):
        self.repository = repository

    async def create_notion_files(
        self, notion_raw_files: List[NotionPage], user_id: UUID, sync_user_id: int
    ) -> list[NotionSyncFile]:
        pages_to_add: List[NotionSyncFile] = []
        for page in notion_raw_files:
            if (
                (page.in_trash is None or not page.in_trash)
                and not page.archived
                and page.parent.type in ("page_id", "workspace")
            ):
                pages_to_add.append(page.to_syncfile(user_id, sync_user_id))
        inserted_notion_files = await self.repository.create_notion_files(pages_to_add)
        logger.info(f"Insert response {inserted_notion_files}")
        return pages_to_add

    async def update_notion_files(
        self,
        notion_pages: List[NotionPage],
        user_id: UUID,
        sync_user_id: int,
        client: Client,
    ) -> bool:
        # 1. For each page we check if it is already in the db, if it is we modify it, if it isn't we create it.
        # 2. If the page was modified, we check all direct children of the page and check if they stil exist in notion, if they don't, we delete it
        # 3. We check if the root folder was deleted, if so we delete the root page & all children
        try:
            pages_to_delete: list[UUID] = []
            for page in notion_pages:
                if (
                    not page.in_trash
                    and not page.archived
                    and page.parent.type != "database_id"
                ):
                    logger.debug(
                        "Updating notion file %s ",
                        page.id,
                    )
                    is_update = await self.repository.update_notion_file(
                        page.to_syncfile(user_id, sync_user_id)
                    )

                    if is_update:
                        logger.info(
                            f"Updated notion file {page.id}, we need to check if children were deleted"
                        )
                        children = await self.get_notion_files_by_parent_id(
                            str(page.id),
                            sync_user_id,
                        )
                        for child in children:
                            try:
                                child_notion_page = client.pages.retrieve(
                                    str(child.notion_id)
                                )
                                if (
                                    child_notion_page["archived"]
                                    or child_notion_page["in_trash"]
                                ):
                                    pages_to_delete.append(child.notion_id)
                            except Exception:
                                logger.error(
                                    f"Page {child.notion_id} is in trash or archived, we are deleting it."
                                )
                                pages_to_delete.append(child.notion_id)

                else:
                    logger.info(f"Page {page.id} is in trash or archived, skipping ")

            root_pages = await self.get_root_notion_files(sync_user_id=sync_user_id)

            for root_page in root_pages:
                root_notion_page = client.pages.retrieve(root_page.notion_id)
                if root_notion_page["archived"] or root_notion_page["in_trash"]:
                    pages_to_delete.append(root_page.notion_id)
            logger.info(f"Pages to delete: {pages_to_delete}")
            await self.repository.delete_notion_pages(pages_to_delete)

            return True
        except Exception as e:
            logger.error(f"Error updating notion pages: {e}")
            return False

    async def get_notion_files_by_ids(self, ids: List[str]) -> Sequence[NotionSyncFile]:
        logger.info(f"Fetching notion files for IDs: {ids}")
        notion_files = await self.repository.get_notion_files_by_ids(ids)
        logger.info(f"Fetched {len(notion_files)} notion files")
        return notion_files

    async def get_notion_files_by_parent_id(
        self, parent_id: str | None, sync_user_id: int
    ) -> Sequence[NotionSyncFile]:
        logger.info(f"Fetching notion files with parent_id: {parent_id}")
        notion_files = await self.repository.get_notion_files_by_parent_id(
            parent_id, sync_user_id
        )
        logger.info(
            f"Fetched {len(notion_files)} notion files with parent_id {parent_id}"
        )
        return notion_files

    async def get_root_notion_files(
        self, sync_user_id: int
    ) -> Sequence[NotionSyncFile]:
        logger.info("Fetching root notion files")
        notion_files = await self.repository.get_notion_files_by_parent_id(
            None, sync_user_id
        )
        logger.info(f"Fetched {len(notion_files)} root notion files")
        return notion_files

    async def is_folder_page(self, page_id: str) -> bool:
        logger.info(f"Checking if page is a folder: {page_id}")
        is_folder = await self.repository.is_folder_page(page_id)
        return is_folder

    async def delete_notion_pages(self, page_id: UUID):
        await self.repository.delete_notion_page(page_id)


async def update_notion_pages(
    notion_service: SyncNotionService,
    pages_to_update: list[NotionPage],
    user_id: UUID,
    sync_user_id: int,
    client: Client,
):
    return await notion_service.update_notion_files(
        pages_to_update, user_id, sync_user_id, client
    )


async def store_notion_pages(
    all_search_result: list[NotionPage],
    notion_service: SyncNotionService,
    user_id: UUID,
    sync_user_id: int,
):
    return await notion_service.create_notion_files(
        all_search_result, user_id, sync_user_id
    )


def fetch_notion_pages(
    notion_client: Client, start_cursor: str | None = None
) -> NotionSearchResult:
    search_result = notion_client.search(
        query="",
        filter={"property": "object", "value": "page"},
        sort={"direction": "descending", "timestamp": "last_edited_time"},
        start_cursor=start_cursor,
    )
    return NotionSearchResult.model_validate(search_result)


def fetch_limit_notion_pages(
    notion_client: Client,
    last_sync_time: datetime,
) -> List[NotionPage]:
    all_search_result = []
    last_sync_time = last_sync_time.astimezone(timezone.utc)

    search_result = fetch_notion_pages(notion_client)
    for page in search_result.results:
        if page.last_edited_time > last_sync_time:
            all_search_result.append(page)

    if last_sync_time > page.last_edited_time:
        return all_search_result

    while search_result.has_more:
        logger.debug("next page cursor: %s", search_result.next_cursor)  # type: ignore
        search_result = fetch_notion_pages(
            notion_client, start_cursor=search_result.next_cursor
        )

        for page in search_result.results:
            if page.last_edited_time > last_sync_time:
                all_search_result.append(page)

        if last_sync_time > page.last_edited_time:
            return all_search_result

    return all_search_result
