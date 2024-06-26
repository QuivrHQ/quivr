from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Knowledge(BaseModel):
    id: UUID
    brain_id: UUID
    file_name: Optional[str] = None
    url: Optional[str] = None
    extension: str = "txt"
