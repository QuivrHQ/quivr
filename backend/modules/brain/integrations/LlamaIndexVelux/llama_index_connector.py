import os
import tempfile
from io import BytesIO
from typing import Any, List

from celery_config import celery
from fastapi import UploadFile
from logger import get_logger
from modules.brain.entity.integration_brain import IntegrationEntity
from modules.brain.repository.integration_brains import Integration, IntegrationBrain
from modules.knowledge.dto.inputs import CreateKnowledgeProperties
from modules.knowledge.repository.knowledge_interface import KnowledgeInterface
from modules.knowledge.service.knowledge_service import KnowledgeService
from pydantic import BaseModel
from repository.files.upload_file import upload_file_storage

logger = get_logger(__name__)


class LlamaIndexPage(BaseModel):
    """Represents a LlamaIndex Page object"""

    id: str
    created_time: str
    last_edited_time: str
    archived: bool
    properties: dict[str, Any]
    url: str


class LlamaIndexConnector(IntegrationBrain, Integration):
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
        logger.info(f"Adding file to knowledge: {page_name}")
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
                response = upload_file_storage(
                    temp_file_path, filename_with_brain_id, "true"
                )
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
                        "delete_file": True,
                    },
                )
        except Exception:
            logger.error("Error adding knowledge")

    def load(self):
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

    def poll(self):
        """
        Update all the brains with the latest data from Notion
        """
        integration = self.get_integration_brain(self.brain_id, self.user_id)
        last_synced = integration.last_synced

        query_dict = {
            "page_size": self.max_pages,
            "sort": {"timestamp": "last_edited_time", "direction": "descending"},
            "filter": {"property": "object", "value": "page"},
        }
        documents = []

        while True:
            db_res = self._search_notion(query_dict)
            pages = self._filter_pages_by_time(
                db_res.results, last_synced, filter_field="last_edited_time"
            )
            for page in pages:
                logger.info(f"Reading page: {page.id}")
                page_title, page_content, child_pages, page_url = self._read_page(
                    page.id
                )
                document = {
                    "page_title": page_title,
                    "page_content": page_content,
                    "child_pages": child_pages,
                    "page_url": page_url,
                }
                documents.append(document)
                self.add_file_to_knowledge(page_content, page_title, page_url)
            if not db_res.has_more:
                break
            query_dict["start_cursor"] = db_res.next_cursor
        logger.info(
            f"last Synced: {self.update_last_synced(self.brain_id, self.user_id)}"
        )
        return documents


if __name__ == "__main__":

    notion = NotionConnector(
        brain_id="73f7d092-d596-4fd0-b24f-24031e9b53cd",
        user_id="39418e3b-0258-4452-af60-7acfcc1263ff",
    )

    print(notion.poll())
