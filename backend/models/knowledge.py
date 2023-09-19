from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Knowledge(BaseModel):
    id: Optional[UUID] = None
    brain_id: Optional[UUID] = None
    file_name: Optional[str] = None
    url: Optional[str] = None
    extension: str = "txt"
