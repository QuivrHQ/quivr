from datetime import datetime

from pydantic import BaseModel


class SyncsActive(BaseModel):
    id: int
    name: str
    syncs_user_id: int
    user_id: str
    settings: dict
    last_synced: datetime
    sync_interval_minutes: int
    brain_id: str


class SyncsFiles(BaseModel):
    id: int
    path: str
    syncs_active_id: int
    last_modified: str
    brain_id: str
