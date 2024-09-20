from typing import Dict, Optional
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
    parent_id: Optional[UUID] = None


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


class LinkKnowledge(BaseModel):
    knowledge: KnowledgeDTO
