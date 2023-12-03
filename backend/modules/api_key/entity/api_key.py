from pydantic import BaseModel


class ApiKey(BaseModel):
    api_key: str
    key_id: str
    days: int
    only_chat: bool
    name: str
    creation_time: str
    is_active: bool
