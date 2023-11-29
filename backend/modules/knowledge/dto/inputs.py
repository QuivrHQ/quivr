from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CreateKnowledgeProperties(BaseModel):
    brain_id: UUID
    file_name: Optional[str] = None
    url: Optional[str] = None
    extension: str = "txt"

    def dict(self, *args, **kwargs):
        knowledge_dict = super().dict(*args, **kwargs)
        knowledge_dict["brain_id"] = str(knowledge_dict.get("brain_id"))
        return knowledge_dict
