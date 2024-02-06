import os
import tempfile
from io import BytesIO
from typing import Any, List, Optional

import requests
from celery_config import celery
from fastapi import UploadFile
from logger import get_logger
from modules.brain.entity.integration_brain import IntegrationEntity
from modules.brain.repository.integration_brains import IntegrationBrain
from modules.knowledge.dto.inputs import CreateKnowledgeProperties
from modules.knowledge.repository.knowledge_interface import KnowledgeInterface
from modules.knowledge.service.knowledge_service import KnowledgeService
from pydantic import BaseModel
from repository.files.upload_file import upload_file_storage

logger = get_logger(__name__)


class NotionPage(BaseModel):
    """Represents a Notion Page object"""

    id: str
    created_time: str
    last_edited_time: str
    archived: bool
    properties: dict[str, Any]
    url: str


class NotionSearchResponse(BaseModel):
    """Represents the response from the Notion Search API"""

    results: list[dict[str, Any]]
    next_cursor: Optional[str]
    has_more: bool = False


class NotionConnector(IntegrationBrain):
    """A class to interact with the Notion API"""

    credentials: dict[str, str] = None
    integration_details: IntegrationEntity = None
    brain_id: str = None
    user_id: str = None
    knowledge_service: KnowledgeInterface
    recursive_index_enabled: bool = False
    max_pages: int = 100

    def __init__(self, brain_id: str, user_id: str):
        super().__init__()
        self.brain_id = brain_id
        self.user_id = user_id
        self._load_credentials()
        self.knowledge_service = KnowledgeService()

    def _load_credentials(self) -> dict[str, str]:
        """Load the Notion credentials"""
        self.integration_details = self.get_integration_brain(
            self.brain_id, self.user_id
        )
        if self.credentials is None:
            logger.info("Loading Notion credentials")
            self.integration_details.credentials = {
                "notion_integration_token": self.integration_details.settings.get(
                    "notion_integration_token", ""
                )
            }
            self.update_integration_brain(
                self.brain_id, self.user_id, self.integration_details
            )
            self.credentials = self.integration_details.credentials
        else:  # pragma: no cover
            self.credentials = self.integration_details.credentials

    def _headers(self) -> dict[str, str]:
        """Get the headers for the Notion API"""
        return {
            "Authorization": f'Bearer {self.credentials["notion_integration_token"]}',
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def _search_notion(self, query_dict: dict[str, Any]) -> NotionSearchResponse:
        """
        Search for pages from a Notion database.
        """
        # Use self.credentials to authenticate the request
        headers = self._headers()
        res = requests.post(
            "https://api.notion.com/v1/search",
            headers=headers,
            json=query_dict,
            # Adjust the timeout as needed
            timeout=10,
        )
        res.raise_for_status()
        return NotionSearchResponse(**res.json())

    def _fetch_blocks(self, page_id: str, cursor: str | None = None) -> dict[str, Any]:
        """
        Fetch the blocks of a Notion page.
        """
        logger.info(f"Fetching blocks for page: {page_id}")
        headers = self._headers()
        query_params = None if not cursor else {"start_cursor": cursor}
        res = requests.get(
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            params=query_params,
            headers=headers,
            timeout=10,
        )
        res.raise_for_status()
        return res.json()

    def _fetch_page(self, page_id: str) -> dict[str, Any]:
        """
        Fetch a Notion page.
        """
        logger.info(f"Fetching page: {page_id}")
        headers = self._headers()
        block_url = f"https://api.notion.com/v1/pages/{page_id}"
        res = requests.get(
            block_url,
            headers=headers,
            timeout=10,
        )
        try:
            res.raise_for_status()
        except Exception:
            logger.exception(f"Error fetching page - {res.json()}")
            return None
        return NotionPage(**res.json())

    def _read_blocks(
        self, page_block_id: str
    ) -> tuple[list[tuple[str, str]], list[str]]:
        """Reads blocks for a page"""
        result_lines: list[tuple[str, str]] = []
        child_pages: list[str] = []
        cursor = None
        while True:
            data = self._fetch_blocks(page_block_id, cursor)

            for result in data["results"]:
                result_block_id = result["id"]
                result_type = result["type"]
                result_obj = result[result_type]

                cur_result_text_arr = []
                if "rich_text" in result_obj:
                    for rich_text in result_obj["rich_text"]:
                        # skip if doesn't have text object
                        if "text" in rich_text:
                            text = rich_text["text"]["content"]
                            cur_result_text_arr.append(text)

                if result["has_children"]:
                    if result_type == "child_page":
                        child_pages.append(result_block_id)
                    else:
                        logger.info(f"Entering sub-block: {result_block_id}")
                        subblock_result_lines, subblock_child_pages = self._read_blocks(
                            result_block_id
                        )
                        logger.info(f"Finished sub-block: {result_block_id}")
                        result_lines.extend(subblock_result_lines)
                        child_pages.extend(subblock_child_pages)

                # if result_type == "child_database" and self.recursive_index_enabled:
                #     child_pages.extend(self._read_pages_from_database(result_block_id))

                cur_result_text = "\n".join(cur_result_text_arr)
                if cur_result_text:
                    result_lines.append((cur_result_text, result_block_id))

            if data["next_cursor"] is None:
                break

            cursor = data["next_cursor"]

        return result_lines, child_pages

    def _read_page_title(self, page: NotionPage) -> str:
        """Extracts the title from a Notion page"""
        page_title = None
        for _, prop in page.properties.items():
            if prop["type"] == "title" and len(prop["title"]) > 0:
                page_title = " ".join([t["plain_text"] for t in prop["title"]]).strip()
                break
        if page_title is None:
            page_title = f"Untitled Page [{page.id}]"
        page_title = "".join(e for e in page_title if e.isalnum())
        return page_title

    def _read_page_url(self, page: NotionPage) -> str:
        """Extracts the URL from a Notion page"""
        return page.url

    def _read_pages_from_database(self, database_id: str) -> list[str]:
        """Reads pages from a Notion database"""
        headers = self._headers()
        res = requests.post(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            headers=headers,
            timeout=10,
        )
        res.raise_for_status()
        return [page["id"] for page in res.json()["results"]]

    def _read_page(self, page_id: str) -> tuple[str, list[str]]:
        """Reads a Notion page"""
        page = self._fetch_page(page_id)
        if page is None:
            return None, None, None, None
        page_title = self._read_page_title(page)
        page_content, child_pages = self._read_blocks(page_id)
        page_url = self._read_page_url(page)
        return page_title, page_content, child_pages, page_url

    def get_all_pages(self) -> list[NotionPage]:
        """
        Get all the pages from Notion.
        """
        query_dict = {
            "filter": {"property": "object", "value": "page"},
            "page_size": 100,
        }
        max_pages = self.max_pages
        pages_count = 0
        while True:
            search_response = self._search_notion(query_dict)
            for page in search_response.results:
                pages_count += 1
                if pages_count > max_pages:
                    break
                yield NotionPage(**page)

            if search_response.has_more:
                query_dict["start_cursor"] = search_response.next_cursor
            else:
                break

    def add_file_to_knowledge(
        self, page_content: List[tuple[str, str]], page_name: str, page_url: str
    ):
        """
        Add a file to the knowledge base
        """
        filename_with_brain_id = (
            str(self.brain_id) + "/" + str(page_name) + "_notion.txt"
        )
        try:
            concatened_page_content = ""
            if page_content:
                for content in page_content:
                    concatened_page_content += content[0] + "\n"

                # Create a BytesIO object from the content
                content_io = BytesIO(concatened_page_content.encode("utf-8"))

                # Create a file of type UploadFile
                file = UploadFile(filename=filename_with_brain_id, file=content_io)

                # Write the UploadFile content to a temporary file
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(file.file.read())
                    temp_file_path = temp_file.name

                # Upload the temporary file to the knowledge base
                response = upload_file_storage(temp_file_path, filename_with_brain_id)
                logger.info(f"File {response} uploaded successfully")

                # Delete the temporary file
                os.remove(temp_file_path)

                knowledge_to_add = CreateKnowledgeProperties(
                    brain_id=self.brain_id,
                    file_name=page_name + "_notion.txt",
                    extension="txt",
                    integration="notion",
                    integration_link=page_url,
                )

                added_knowledge = self.knowledge_service.add_knowledge(knowledge_to_add)
                logger.info(f"Knowledge {added_knowledge} added successfully")

                celery.send_task(
                    "process_file_and_notify",
                    kwargs={
                        "file_name": filename_with_brain_id,
                        "file_original_name": page_name + "_notion.txt",
                        "brain_id": self.brain_id,
                    },
                )
        except Exception:
            logger.error("Error adding knowledge")

    def compile_all_pages(self):
        """
        Get all the pages, blocks, databases from Notion into a single document per page
        """
        all_pages = list(self.get_all_pages())  # Convert generator to list
        documents = []
        for page in all_pages:
            logger.info(f"Reading page: {page.id}")
            page_title, page_content, child_pages, page_url = self._read_page(page.id)
            document = {
                "page_title": page_title,
                "page_content": page_content,
                "child_pages": child_pages,
                "page_url": page_url,
            }
            documents.append(document)
            self.add_file_to_knowledge(page_content, page_title, page_url)
        return documents


if __name__ == "__main__":

    notion = NotionConnector(
        brain_id="b3ab23c5-9e13-4dd8-8883-106d613e3de8",
        user_id="39418e3b-0258-4452-af60-7acfcc1263ff",
    )

    celery.send_task(
        "NotionConnectorLoad",
        kwargs={
            "brain_id": "b3ab23c5-9e13-4dd8-8883-106d613e3de8",
            "user_id": "39418e3b-0258-4452-af60-7acfcc1263ff",
        },
    )
