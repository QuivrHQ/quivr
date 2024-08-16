from datetime import datetime, timedelta
from typing import Any, List, Sequence
from uuid import UUID

from notion_client import Client

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseService
from quivr_api.modules.sync.entity.sync_models import NotionSyncFile
from quivr_api.modules.sync.repository.sync_repository import NotionRepository

logger = get_logger(__name__)


class SyncNotionService(BaseService[NotionRepository]):
    repository_cls = NotionRepository

    def __init__(self, repository: NotionRepository):
        self.repository = repository

    async def create_notion_files(
        self, notion_raw_files: List[dict[str, Any]], user_id: UUID
    ) -> list[NotionSyncFile]:
        pages_to_add: List[NotionSyncFile] = []
        for page in notion_raw_files:
            parent_type = page["parent"]["type"]
            if (
                not page["in_trash"]
                and not page["archived"]
                and page["parent"]["type"] != "database_id"
            ):
                file = NotionSyncFile(
                    notion_id=page["id"],
                    parent_id=(
                        page["parent"][parent_type]
                        if not parent_type == "workspace"
                        else None
                    ),
                    name=f'{page["properties"]["title"]["title"][0]["text"]["content"]}.md',
                    icon=page["icon"]["emoji"]
                    if "icon" in page and "emoji" in page["icon"]
                    else None,
                    mime_type="md",
                    web_view_link=page["url"],
                    is_folder=True,
                    last_modified=datetime.strptime(
                        page["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    type="page",
                    user_id=user_id,
                )
                pages_to_add.append(file)
        inserted_notion_files = await self.repository.create_notion_files(pages_to_add)
        logger.info(f"Insert response {inserted_notion_files}")
        return pages_to_add

    async def update_notion_files(
        self, notion_raw_files: List[dict[str, Any]], user_id: UUID, client: Client
    ) -> bool:
        try:
            pages_to_delete: list[str] = []

            # 1. For each page we check if it is already in the db, if it is we modify it, if it isn't we create it.
            # 2. If the page was modified, we check all direct children of the page and check if they stil exist in notion, if they don't, we delete it
            # 3. We check if the root folder was deleted, if so we delete the root page & all children

            for page in notion_raw_files:
                parent_type = page["parent"]["type"]
                if (
                    not page["in_trash"]
                    and not page["archived"]
                    and page["parent"]["type"] != "database_id"
                ):
                    logger.debug(
                        "Updating notion file %s ",
                        page["properties"]["title"]["title"][0]["text"]["content"],
                    )
                    file = NotionSyncFile(
                        notion_id=page["id"],
                        parent_id=page["parent"][parent_type],
                        name=f'{page["properties"]["title"]["title"][0]["text"]["content"]}.md',
                        icon=page["icon"]["emoji"]
                        if "icon" in page and "emoji" in page["icon"]
                        else None,
                        mime_type="md",
                        web_view_link=page["url"],
                        is_folder=True,
                        last_modified=datetime.strptime(
                            page["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        ),
                        type="page",
                        user_id=user_id,
                    )
                    is_update = await self.repository.update_notion_file(file)

                    if is_update:
                        logger.info(
                            f"Updated notion file {file.notion_id}, we need to check if children were deleted"
                        )
                        children = await self.get_notion_files_by_parent_id(
                            file.notion_id
                        )
                        for child in children:
                            try:
                                child_notion_page = client.pages.retrieve(
                                    child.notion_id
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
                    logger.info(
                        f"Page {page['id']} is in trash or archived, skipping i guess"
                    )

            root_pages = await self.get_root_notion_files()

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
        self, parent_id: str | None
    ) -> Sequence[NotionSyncFile]:
        logger.info(f"Fetching notion files with parent_id: {parent_id}")
        notion_files = await self.repository.get_notion_files_by_parent_id(parent_id)
        logger.info(
            f"Fetched {len(notion_files)} notion files with parent_id {parent_id}"
        )
        return notion_files

    async def get_root_notion_files(self) -> Sequence[NotionSyncFile]:
        logger.info("Fetching root notion files")
        notion_files = await self.repository.get_notion_files_by_parent_id(None)
        logger.info(f"Fetched {len(notion_files)} root notion files")
        return notion_files

    async def get_all_notion_files(self) -> Sequence[NotionSyncFile]:
        logger.info("Fetching all notion files")
        notion_files = await self.repository.get_all_notion_files()
        logger.info(f"Fetched {len(notion_files)} notion files")
        return notion_files

    async def is_folder_page(self, page_id: str) -> bool:
        logger.info(f"Checking if page is a folder: {page_id}")
        is_folder = await self.repository.is_folder_page(page_id)
        return is_folder

    async def delete_notion_pages(self, page_id: str):
        await self.repository.delete_notion_file(page_id)


async def update_notion_pages(
    notion_service: SyncNotionService,
    pages_to_update: list[dict[str, Any]],
    user_id: UUID,
    client: Client,
):
    return await notion_service.update_notion_files(pages_to_update, user_id, client)


async def store_notion_pages(
    all_search_result: list[dict[str, Any]],
    notion_service: SyncNotionService,
    user_id: UUID,
):
    return await notion_service.create_notion_files(all_search_result, user_id)


def fetch_notion_pages(
    notion_client: Client,
    last_sync_time: datetime = datetime.now() - timedelta(hours=6),
) -> List[dict[str, Any]]:
    all_search_result = []

    search_result = notion_client.search(
        query="",
        filter={"property": "object", "value": "page"},
        sort={"direction": "descending", "timestamp": "last_edited_time"},
    )
    last_edited_time: datetime | None = None

    for page in search_result["results"]:
        last_edited_time = datetime.strptime(
            page["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        if last_edited_time > last_sync_time:
            all_search_result.append(page)

    if last_edited_time and last_edited_time < last_sync_time:
        # We check if the last element of the search result is older than 6 hours, if it is, we stop the search
        return all_search_result

    while search_result["has_more"]:  # type: ignore
        logger.debug("Next cursor: %s", search_result["next_cursor"])  # type: ignore

        search_result = notion_client.search(
            query="",
            filter={"property": "object", "value": "page"},
            sort={"direction": "descending", "timestamp": "last_edited_time"},
            start_cursor=search_result["next_cursor"],  # type: ignore
        )
        for page in search_result["results"]:
            last_edited_time = datetime.strptime(
                page["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            if last_edited_time > last_sync_time:
                all_search_result.append(page)

        if last_edited_time and last_edited_time < last_sync_time:
            # We check if the last element of the search result is older than 6 hours, if it is, we stop the search
            return all_search_result

    return all_search_result
