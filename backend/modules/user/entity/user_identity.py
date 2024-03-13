from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserIdentity(BaseModel):
    id: UUID
    email: Optional[str] = None
    username: Optional[str] = None
    company: Optional[str] = None
    onboarded: Optional[bool] = None
