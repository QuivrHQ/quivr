from typing import List, Optional

from pydantic import BaseModel


class BrainInput(BaseModel):
    required: Optional[bool] = True
    description: str
    type: str


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
    brain: Optional[BrainInput] = None


class Pricing(BaseModel):
    cost: int = 20
    description: str = "Credits per use"


class AssistantOutput(BaseModel):
    id: int
    name: str
    description: str
    pricing: Optional[Pricing] = Pricing()
    tags: Optional[List[str]] = []
    input_description: str
    output_description: str
    inputs: Inputs
    icon_url: Optional[str] = None
