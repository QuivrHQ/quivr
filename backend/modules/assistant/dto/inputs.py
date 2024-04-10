from typing import List
from uuid import UUID

from pydantic import BaseModel


class InputFile(BaseModel):
    allowed_extensions: List[str]
    required: bool
    description: str


class InputUrl(BaseModel):
    required: bool
    description: bool


class InputText(BaseModel):
    required: bool
    description: bool


class Inputs(BaseModel):
    files: List[InputFile]
    urls: List[InputUrl]
    texts: List[InputText]


class OutputEmail(BaseModel):
    required: bool
    description: str
    type: str


class OutputBrain(BaseModel):
    required: bool
    description: str
    type: UUID


class Outputs(BaseModel):
    emails: OutputEmail
    brains: OutputBrain


class Outputs(BaseModel):
    files: List[InputFile]
    urls: List[InputUrl]
    texts: List[InputText]


class AssistantOutput(BaseModel):
    name: str
    input_description: str
    output_description: str
    inputs: Inputs
    outputs: Outputs
