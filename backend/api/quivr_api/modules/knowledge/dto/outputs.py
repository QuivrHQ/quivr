from datetime import datetime
from typing import Any, Dict, List, Optional, Self
from uuid import UUID

from pydantic import BaseModel
from quivr_core.models import KnowledgeStatus


class DeleteKnowledgeResponse(BaseModel):
    file_name: str | None = None
    status: str = "DELETED"
    knowledge_id: UUID


class KnowledgeOut(BaseModel):
    id: UUID
    file_size: int = 0
    status: KnowledgeStatus
    file_name: Optional[str] = None
    url: Optional[str] = None
    extension: str = ".txt"
    is_folder: bool = False
    updated_at: datetime
    created_at: datetime
    source: Optional[str] = None
    source_link: Optional[str] = None
    file_sha1: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    user_id: UUID
    brains: List[Dict[str, Any]]
    parent: Optional[Self]
    children: Optional[list[Self]]
