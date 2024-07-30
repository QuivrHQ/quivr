from datetime import datetime
from typing import Any
from uuid import UUID

from notion_client import Client

from quivr_api.logger import get_logger
from quivr_api.modules.sync.entity.sync import NotionSyncFile
from quivr_api.modules.sync.service.sync_service import SyncNotionService

logger = get_logger(__name__)


# FIXME (@chloedia)
# class NotionPage(BaseModel): ...


def store_notion_pages(
    all_search_result: list[dict[str, Any]],
    notion_service: SyncNotionService,
    user_id: UUID,
):
    for i, page in enumerate(all_search_result):
        logger.debug(f"Processing page: {i}")
        page = all_search_result[i]
        logger.debug(f"Page: {page}")
        parent_type = page["parent"]["type"]
        if (
            page["in_trash"] == False
            and page["archived"] == False
            and page["parent"]["type"] != "database_id"
        ):
            notion_sync_input = NotionSyncFile(
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
            logger.debug(f"Notion sync input: {notion_sync_input}")
            # TODO : service should create the NotionSyncFile object internally
            notion_service.create_notion_file(notion_sync_input)
            logger.debug(f"Created Notion file: {notion_sync_input}")
        else:
            logger.debug(f"Page did not pass filter: {page['id']}")


def fetch_notion_pages(notion_client: Client):
    all_search_result = []
    search_result = notion_client.search(
        query="",
        filter={"property": "object", "value": "page"},
        sort={"direction": "descending", "timestamp": "last_edited_time"},
    )
    all_search_result += search_result["results"]

    while search_result["has_more"]:
        logger.debug("Next cursor: %s", search_result["next_cursor"])

        search_result = notion_client.search(
            query="",
            filter={"property": "object", "value": "page"},
            sort={"direction": "descending", "timestamp": "last_edited_time"},
            start_cursor=search_result["next_cursor"],
        )
        all_search_result += search_result["results"]
    logger.debug(all_search_result[:10], "\n Length: ", len(all_search_result))

    return all_search_result
