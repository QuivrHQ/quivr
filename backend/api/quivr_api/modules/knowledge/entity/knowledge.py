from datetime import datetime
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Knowledge(BaseModel):
    id: UUID
    brain_id: UUID
    file_name: Optional[str] = None
    url: Optional[str] = None
    extension: str = "txt" 
    status: str
    source: Optional[str] = None
    source_link: Optional[str] = None 
    file_size: Optional[int] = None 
    file_sha1: Optional[str] = None  
    updated_at: Optional[datetime] = None 
    created_at: Optional[datetime] = None
    metadata: Optional[Dict[str, str]] = None

    def dict(self, *args, **kwargs):
        knowledge_dict = super().dict(*args, **kwargs)
        knowledge_dict["brain_id"] = str(knowledge_dict.get("brain_id"))
        return knowledge_dict


class KnowledgeDB(SQLModel, table=True):
    id: Optional[UUID] = Field(default=None, primary_key=True)
    brain_id: UUID = Field(..., nullable=False)
    file_name: Optional[str] = Field(default=None, max_length=255)
    url: Optional[str] = Field(default=None, max_length=2048)
    mime_type: str = Field(default="txt", max_length=100)
    status: str = Field(..., max_length=50)
    source: str = Field(..., max_length=255)
    source_link: str = Field(..., max_length=2048)
    file_size: int = Field(..., gt=0)
    file_sha1: str = Field(..., max_length=40)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, str]] = Field(default=None)


