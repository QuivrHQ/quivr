from typing import Any, Optional

from modules.brain.knowledge_brain_qa import KnowledgeBrainQA
from modules.brain.repository.integration_brains import IntegrationBrain
from pydantic import BaseModel, fields


class NotionPage(BaseModel):
    """Represents a Notion Page object"""

    id: str
    created_time: str
    last_edited_time: str
    archived: bool
    properties: dict[str, Any]
    url: str

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)


class NotionSearchResponse(BaseModel):
    """Represents the response from the Notion Search API"""

    results: list[dict[str, Any]]
    next_cursor: Optional[str]
    has_more: bool = False

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        names = set([f.name for f in fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)


class NotionBrainIntegration(IntegrationBrain, KnowledgeBrainQA):
    """Notion Brain Integration"""

    def __init__(
        self, brain_id: str, brain_name: str, brain_type: str, brain_url: str
    ) -> None:
        super().__init__(brain_id, brain_name, brain_type, brain_url)

    def search(
        self, query: str, page_size: int, cursor: Optional[str] = None
    ) -> NotionSearchResponse:
        """Search for a query in Notion"""
