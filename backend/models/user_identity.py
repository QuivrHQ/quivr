from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserIdentity(BaseModel):
    user_id: UUID
    openai_api_key: Optional[str] = None
