from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class AuthMethodEnum(str, Enum):
    URI_WITH_CALLBACK = "uri_with_callback"


class SyncProvider(str, Enum):
    GOOGLE = "google"
    AZURE = "azure"
    DROPBOX = "dropbox"
    NOTION = "notion"
    GITHUB = "github"


class SyncsDescription(BaseModel):
    name: str
    description: str
    auth_method: AuthMethodEnum


class SyncsOutput(BaseModel):
    id: int
    user_id: UUID
    provider: SyncProvider
    state: dict | None
    credentials: dict | None
    additional_data: dict | None
