from pydantic import BaseModel


class ApiKey(BaseModel):
    api_key: str
    key_id: str
