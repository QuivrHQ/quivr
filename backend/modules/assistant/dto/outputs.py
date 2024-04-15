from typing import List, Optional

from pydantic import BaseModel


class InputFile(BaseModel):
    key: str
    allowed_extensions: Optional[List[str]] = ["pdf"]
    required: Optional[bool] = True
    description: str


class InputUrl(BaseModel):
    key: str
    required: Optional[bool] = True
    description: str


class InputText(BaseModel):
    key: str
    required: Optional[bool] = True
    description: str
    validation_regex: Optional[str] = None


class InputBoolean(BaseModel):
    key: str
    required: Optional[bool] = True
    description: str


class InputNumber(BaseModel):
    key: str
    required: Optional[bool] = True
    description: str
    min: Optional[int] = None
    max: Optional[int] = None
    increment: Optional[int] = None
    default: Optional[int] = None


class InputSelectText(BaseModel):
    key: str
    required: Optional[bool] = True
    description: str
    options: List[str]
    default: Optional[str] = None


class InputSelectNumber(BaseModel):
    key: str
    required: Optional[bool] = True
    description: str
    options: List[int]
    default: Optional[int] = None


class Inputs(BaseModel):
    files: Optional[List[InputFile]] = None
    urls: Optional[List[InputUrl]] = None
    texts: Optional[List[InputText]] = None
    booleans: Optional[List[InputBoolean]] = None
    numbers: Optional[List[InputNumber]] = None
    select_texts: Optional[List[InputSelectText]] = None
    select_numbers: Optional[List[InputSelectNumber]] = None


class OutputEmail(BaseModel):
    required: Optional[bool] = True
    description: str
    type: str


class OutputBrain(BaseModel):
    required: Optional[bool] = True
    description: str
    type: str


class Outputs(BaseModel):
    email: Optional[OutputEmail] = None
    brain: Optional[OutputBrain] = None


class AssistantOutput(BaseModel):
    name: str
    description: str
    tags: Optional[List[str]] = []
    input_description: str
    output_description: str
    inputs: Inputs
    outputs: Outputs
    icon_url: Optional[str] = None
