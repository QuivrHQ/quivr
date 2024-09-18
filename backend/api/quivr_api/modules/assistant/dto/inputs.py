from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, root_validator


class CreateTask(BaseModel):
    pretty_id: str
    assistant_id: int
    settings: dict


class BrainInput(BaseModel):
    value: Optional[UUID] = None

    @root_validator(pre=True)
    def empty_string_to_none(cls, values):
        for field, value in values.items():
            if value == "":
                values[field] = None
        return values


class FileInput(BaseModel):
    key: str
    value: str


class UrlInput(BaseModel):
    key: str
    value: str


class TextInput(BaseModel):
    key: str
    value: str


class InputBoolean(BaseModel):
    key: str
    value: bool


class InputNumber(BaseModel):
    key: str
    value: int


class InputSelectText(BaseModel):
    key: str
    value: str


class InputSelectNumber(BaseModel):
    key: str
    value: int


class Inputs(BaseModel):
    files: Optional[List[FileInput]] = None
    urls: Optional[List[UrlInput]] = None
    texts: Optional[List[TextInput]] = None
    booleans: Optional[List[InputBoolean]] = None
    numbers: Optional[List[InputNumber]] = None
    select_texts: Optional[List[InputSelectText]] = None
    select_numbers: Optional[List[InputSelectNumber]] = None
    brain: Optional[BrainInput] = None


class InputAssistant(BaseModel):
    id: int
    name: str
    inputs: Inputs
