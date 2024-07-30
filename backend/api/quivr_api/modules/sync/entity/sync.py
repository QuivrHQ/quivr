from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SyncsUser(BaseModel):
    id: int
    user_id: str
    name: str
    provider: str
    credentials: dict
    state: dict
    additional_data: dict


class SyncFile(BaseModel):
    name: str
    id: str
    is_folder: bool
    last_modified: str
    mime_type: str
    web_view_link: str
    notification_id: Optional[str] = None


class SyncsActive(BaseModel):
    id: int
    name: str
    syncs_user_id: int
    user_id: str
    settings: dict
    last_synced: datetime
    sync_interval_minutes: int
    brain_id: str
    syncs_user: Optional[SyncsUser] = None
    notification_id: Optional[str] = None


class SyncsFiles(BaseModel):
    id: int
    path: str
    syncs_active_id: int
    last_modified: str
    brain_id: str
    supported: bool
