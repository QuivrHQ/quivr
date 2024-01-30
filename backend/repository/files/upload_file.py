import json
import os
from multiprocessing import get_logger

from langchain.pydantic_v1 import Field
from langchain.schema import Document
from models import get_supabase_client
from supabase.client import Client

logger = get_logger()

# Mapping of file extensions to MIME types
mime_types = {
    ".txt": "text/plain",
    ".csv": "text/csv",
    ".md": "text/markdown",
    ".markdown": "text/markdown",
    ".telegram": "application/x-telegram",
    ".m4a": "audio/mp4",
    ".mp3": "audio/mpeg",
    ".webm": "audio/webm",
    ".mp4": "video/mp4",
    ".mpga": "audio/mpeg",
    ".wav": "audio/wav",
    ".mpeg": "video/mpeg",
    ".pdf": "application/pdf",
    ".html": "text/html",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".odt": "application/vnd.oasis.opendocument.text",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xls": "application/vnd.ms-excel",
    ".epub": "application/epub+zip",
    ".ipynb": "application/x-ipynb+json",
    ".py": "text/x-python",
}


def upload_file_storage(file, file_identifier: str):
    supabase_client: Client = get_supabase_client()
    response = None

    try:
        # Get the file extension
        _, file_extension = os.path.splitext(file_identifier)

        # Get the MIME type for the file extension
        mime_type = mime_types.get(file_extension, "text/html")

        response = supabase_client.storage.from_("quivr").upload(
            file_identifier, file, file_options={"content-type": mime_type}
        )

        return response
    except Exception as e:
        logger.error(e)
        raise e


class DocumentSerializable(Document):
    """Class for storing a piece of text and associated metadata."""

    page_content: str
    metadata: dict = Field(default_factory=dict)

    @property
    def lc_serializable(self) -> bool:
        return True

    def __repr__(self):
        return f"Document(page_content='{self.page_content[:50]}...', metadata={self.metadata})"

    def __str__(self):
        return self.__repr__()

    def to_json(self) -> str:
        """Convert the Document object to a JSON string."""
        return json.dumps(
            {
                "page_content": self.page_content,
                "metadata": self.metadata,
            }
        )

    @classmethod
    def from_json(cls, json_str: str):
        """Create a Document object from a JSON string."""
        data = json.loads(json_str)
        return cls(page_content=data["page_content"], metadata=data["metadata"])
