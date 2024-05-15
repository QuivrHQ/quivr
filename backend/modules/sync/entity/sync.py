from pydantic import BaseModel
from datetime import datetime

class SyncsActive(BaseModel):
    id: int
    name: str
    id_syncs_user: int
    user_id: str
    settings: dict
    last_synced: datetime
    sync_interval_minutes: int