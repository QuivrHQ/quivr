from pydantic import BaseModel


class ApiKeyInfo(BaseModel):
    key_id: str
    creation_time: str
