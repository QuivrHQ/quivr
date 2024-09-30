from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel
from quivr_core.models import KnowledgeStatus

from quivr_api.modules.knowledge.dto.outputs import KnowledgeDTO


class CreateKnowledgeProperties(BaseModel):
    brain_id: UUID
    file_name: Optional[str] = None
    url: Optional[str] = None
    extension: str = ".txt"
    status: KnowledgeStatus = KnowledgeStatus.PROCESSING
    source: str = "local"
    source_link: Optional[str] = None
    file_size: Optional[int] = None
    file_sha1: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    is_folder: bool = False
    parent_id: Optional[UUID] = None


class AddKnowledge(BaseModel):
    file_name: Optional[str] = None
    url: Optional[str] = None
    extension: str = ".txt"
    source: str = "local"
    source_link: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    is_folder: bool = False
    parent_id: UUID | None = None
    sync_id: int | None = None
    sync_file_id: str | None = None


class KnowledgeUpdate(BaseModel):
    file_name: Optional[str] = None
    status: Optional[KnowledgeStatus] = None
    url: Optional[str] = None
    file_sha1: Optional[str] = None
    extension: Optional[str] = None
    parent_id: Optional[UUID] = None
    source: Optional[str] = None
    source_link: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


class LinkKnowledgeBrain(BaseModel):
    bulk_id: UUID
    knowledge: KnowledgeDTO
    brain_ids: List[UUID]


class UnlinkKnowledgeBrain(BaseModel):
    knowledge_id: UUID
    brain_ids: List[UUID]
