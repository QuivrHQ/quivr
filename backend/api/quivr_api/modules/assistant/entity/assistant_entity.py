from pydantic import BaseModel
from typing import List


class AssistantInput(BaseModel):
    name: str
    description: str
    type: str


class AssistantSettings(BaseModel):
    inputs: List[AssistantInput]


class Assistant(BaseModel):
    name: str
    description: str
    settings: AssistantSettings
