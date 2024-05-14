from pydantic import BaseModel


class SyncsUserInput(BaseModel):
    user_id: str
    sync_name: str
    credentials: dict
    state: dict


class SyncUserUpdateInput(BaseModel):
    credentials: dict
    state: dict
