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


class ConditionalInput(BaseModel):
    """
    Conditional input is a list of inputs that are conditional to the value of another input.
    key: The key of the input that is conditional.
    conditional_key: The key that determines if the input is shown.
    """

    key: str
    conditional_key: str
    condition: Optional[str] = (
        None  # e.g. "equals", "contains", "starts_with", "ends_with", "regex", "in", "not_in", "is_empty", "is_not_empty"
    )
    value: Optional[str] = None


class Inputs(BaseModel):
    files: Optional[List[InputFile]] = None
    urls: Optional[List[InputUrl]] = None
    texts: Optional[List[InputText]] = None
    booleans: Optional[List[InputBoolean]] = None
    numbers: Optional[List[InputNumber]] = None
    select_texts: Optional[List[InputSelectText]] = None
    select_numbers: Optional[List[InputSelectNumber]] = None
    brain: Optional[BrainInput] = None
    conditional_inputs: Optional[List[ConditionalInput]] = None


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
