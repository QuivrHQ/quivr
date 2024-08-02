from datetime import datetime
from typing import Any, List, Sequence
from uuid import UUID

from notion_client import Client

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import BaseService
from quivr_api.modules.sync.entity.sync import NotionSyncFile
from quivr_api.modules.sync.repository.sync import NotionRepository

logger = get_logger(__name__)


# FIXME (@chloedia)
# class NotionPage(BaseModel): ...


class SyncNotionService(BaseService[NotionRepository]):
    repository_cls = NotionRepository

    def __init__(self, repository: NotionRepository):
        self.repository = repository

    async def create_notion_file(
        self, notion_sync_file: NotionSyncFile
    ) -> NotionSyncFile:
        logger.info(
            f"New notion entry on notion table for user {notion_sync_file.user_id}"
        )

        inserted_notion_file = await self.repository.create_notion_file(
            notion_sync_file
        )
        logger.info(f"Insert response {inserted_notion_file}")

        return inserted_notion_file

    async def update_notion_file(
        self, notion_sync_file: NotionSyncFile
    ) -> NotionSyncFile:
        logger.info(
            f"Updating notion entry on notion table for user {notion_sync_file.user_id}"
        )

        updated_notion_file = await self.repository.update_notion_file(notion_sync_file)
        logger.info(f"Update response {updated_notion_file}")

        return updated_notion_file

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
        notion_files = await self.repository.get_notion_files_by_parent_id("True")
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
    all_search_result: List[dict[str, Any]],
    all_db_pages: Sequence[NotionSyncFile],
    notion_service: SyncNotionService,
    user_id: UUID,
):
    for i, page in enumerate(all_search_result):
        page = all_search_result[i]
        parent_type = page["parent"]["type"]
        if (
            not page["in_trash"]
            and not page["archived"]
            and page["parent"]["type"] != "database_id"
        ):
            # Find notion_id in all_db_pages
            current_page = next(
                (x for x in all_db_pages if x.notion_id == page["id"]), None
            )
            if not current_page or current_page.last_modified.replace(
                tzinfo=None
            ) < datetime.strptime(
                page["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
            ).replace(tzinfo=None):
                logger.info("Page %s was modified", page["id"])

                file = NotionSyncFile(
                    notion_id=page["id"],
                    parent_id=page["parent"][parent_type],
                    name=f'{page["properties"]["title"]["title"][0]["text"]["content"]}.md',
                    icon=page["icon"]["emoji"] if page["icon"] else None,
                    mime_type="md",
                    web_view_link=page["url"],
                    is_folder=True,
                    last_modified=datetime.strptime(
                        page["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                    type="page",
                    user_id=user_id,
                )
                # FIXME(@chloedia): service should create the NotionSyncFile object internally
                # The notion_service should insert ALL the pages in a single batch
                # This loop should live in the notion_service
                await notion_service.update_notion_file(file)
    # check for deleted pages
    for page in all_db_pages:
        if not any(page.notion_id == x["id"] for x in all_search_result):
            logger.info("Deleting page: %s", page.notion_id)
            await notion_service.delete_notion_pages(page.notion_id)

    return True


async def store_notion_pages(
    all_search_result: list[dict[str, Any]],
    notion_service: SyncNotionService,
    user_id: UUID,
):
    notion_sync_files = []
    for i, page in enumerate(all_search_result):
        page = all_search_result[i]
        parent_type = page["parent"]["type"]
        if (
            not page["in_trash"]
            and not page["archived"]
            and page["parent"]["type"] != "database_id"
        ):
            file = NotionSyncFile(
                notion_id=page["id"],
                parent_id=page["parent"][parent_type]
                if not parent_type == "workspace"
                else None,
                name=f'{page["properties"]["title"]["title"][0]["text"]["content"]}.md',
                icon=page["icon"]["emoji"] if page["icon"] else None,
                mime_type="md",
                web_view_link=page["url"],
                is_folder=True,
                last_modified=datetime.strptime(
                    page["last_edited_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ),
                type="page",
                user_id=user_id,
            )
            # FIXME(@chloedia): service should create the NotionSyncFile object internally
            # The notion_service should insert ALL the pages in a single batch
            # This loop should live in the notion_service
            await notion_service.create_notion_file(file)
            notion_sync_files.append(file)
    return notion_sync_files


def fetch_notion_pages(notion_client: Client):
    all_search_result = []
    search_result = notion_client.search(
        query="",
        filter={"property": "object", "value": "page"},
        sort={"direction": "descending", "timestamp": "last_edited_time"},
    )
    end_sync_time = datetime.strptime(
        search_result["results"][-1]["last_edited_time"],
        "%Y-%m-%dT%H:%M:%S.%fZ",  # type: ignore
    )
    all_search_result += search_result["results"]  # type: ignore

    while search_result["has_more"]:  # type: ignore
        logger.debug("Next cursor: %s", search_result["next_cursor"])  # type: ignore

        search_result = notion_client.search(
            query="",
            filter={"property": "object", "value": "page"},
            sort={"direction": "descending", "timestamp": "last_edited_time"},
            start_cursor=search_result["next_cursor"],  # type: ignore
        )
        all_search_result += search_result["results"]  # type: ignore

    return all_search_result
