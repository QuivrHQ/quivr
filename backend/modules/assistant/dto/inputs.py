from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class EmailInput(BaseModel):
    activated: bool


class BrainInput(BaseModel):
    activated: bool
    value: UUID


class FileInput(BaseModel):
    key: str
    value: str


class UrlInput(BaseModel):
    key: str
    value: str


class TextInput(BaseModel):
    key: str
    value: str


class Inputs(BaseModel):
    files: Optional[List[FileInput]] = None
    urls: Optional[List[UrlInput]] = None
    texts: Optional[List[TextInput]] = None


class Outputs(BaseModel):
    email: Optional[EmailInput] = None
    brain: Optional[BrainInput] = None


class InputAssistant(BaseModel):
    name: str
    inputs: Inputs
    outputs: Outputs
