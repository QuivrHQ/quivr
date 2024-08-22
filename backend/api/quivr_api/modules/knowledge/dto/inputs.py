from enum import Enum
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class KnowledgeStatus(str, Enum):
    PROCESSING = "PROCESSING"
    UPLOADED = "UPLOADED"
    ERROR = "ERROR"


class CreateKnowledgeProperties(BaseModel):
    brain_id: UUID
    file_name: Optional[str] = None
    url: Optional[str] = None
    mime_type: str = "application/txt"
    status: KnowledgeStatus = KnowledgeStatus.PROCESSING
    source: str = "local"
    source_link: Optional[str] = None
    file_size: Optional[int] = None
    file_sha1: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None

    def dict(self, *args, **kwargs):
        knowledge_dict = super().dict(*args, **kwargs)
        knowledge_dict["brain_id"] = str(knowledge_dict.get("brain_id"))
        return knowledge_dict
