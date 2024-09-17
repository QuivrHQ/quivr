from pydantic import BaseModel
from typing import List


class AssistantInput(BaseModel):
    name: str
    description: str
    type: str


class AssistantInputOutput(BaseModel):
    name: str
    value: str


class AssistantSettings(BaseModel):
    inputs: List[AssistantInput]


class Assistant(BaseModel):
    id: int
    name: str
    description: str
    settings: AssistantSettings
    file1_name: str
    file2_name: str
