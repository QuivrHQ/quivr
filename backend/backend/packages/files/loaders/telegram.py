from __future__ import annotations

import json
from pathlib import Path
from typing import List

from langchain.docstore.document import Document
from langchain_community.document_loaders.base import BaseLoader


def concatenate_rows(row: dict) -> str:
    """Combine message information in a readable format ready to be used."""
    date = row["date"]
    sender = row.get(
        "from", "Unknown"
    )  # Using .get() to handle cases where 'from' might not be present

    text_content = row.get("text", "")

    # Function to process a single text entity
    def process_text_entity(entity):
        if isinstance(entity, str):
            return entity
        elif isinstance(entity, dict) and "text" in entity:
            return entity["text"]
        return ""

    # Process the text content based on its type
    if isinstance(text_content, str):
        text = text_content
    elif isinstance(text_content, list):
        text = "".join(process_text_entity(item) for item in text_content)
    else:
        text = ""

    # Skip messages with empty text
    if not text.strip():
        return ""

    return f"{sender} on {date}: {text}\n\n"


class TelegramChatFileLoader(BaseLoader):
    """Load from `Telegram chat` dump."""

    def __init__(self, path: str):
        """Initialize with a path."""
        self.file_path = path

    def load(self) -> List[Document]:
        """Load documents."""
        p = Path(self.file_path)

        with open(p, encoding="utf8") as f:
            d = json.load(f)

        text = "".join(
            concatenate_rows(message)
            for message in d["messages"]
            if message["type"] == "message"
            and (isinstance(message["text"], str) or isinstance(message["text"], list))
        )
        metadata = {"source": str(p)}

        return [Document(page_content=text, metadata=metadata)]
