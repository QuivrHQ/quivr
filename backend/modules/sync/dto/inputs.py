from pydantic import BaseModel


class SyncsUserInput(BaseModel):
    user_id: str
    sync_name: str
    credentials: dict
    state: dict


class SyncUserUpdateInput(BaseModel):
    credentials: dict
    state: dict
    
class SyncsActiveInput(BaseModel):
    name: str
    user_id: str
    id_syncs_user: int
    sync_interval_minutes: int
    settings: dict

class SyncsActiveUpdateInput(BaseModel):
    name: str
    sync_interval_minutes: int
    settings: dict
    
