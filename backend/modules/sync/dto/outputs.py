from enum import Enum

from pydantic import BaseModel


class AuthMethodEnum(str, Enum):
    URI_WITH_CALLBACK = "uri_with_callback"


class SyncsDescription(BaseModel):
    name: str
    description: str
    auth_method: AuthMethodEnum


class SyncsUserOutput(BaseModel):
    user_id: str
    provider: str
    state: dict
    credentials: dict
