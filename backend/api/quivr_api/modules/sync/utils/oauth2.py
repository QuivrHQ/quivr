from uuid import UUID

from pydantic import BaseModel


class Oauth2State(BaseModel):
    sync_id: int | None = None
    name: str
    user_id: UUID
