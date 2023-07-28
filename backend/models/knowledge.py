from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Knowledge(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    file_id: Optional[UUID] = None
    url: Optional[str] = None
    content_sha1: Optional[str] = None
    owner_id: Optional[UUID] = None
    summary: Optional[str] = None
    extension: str = "txt"


# compute sha1 from content
