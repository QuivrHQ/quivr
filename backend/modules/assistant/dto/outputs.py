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


class Inputs(BaseModel):
    files: Optional[List[InputFile]] = None
    urls: Optional[List[InputUrl]] = None
    texts: Optional[List[InputText]] = None


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
    input_description: str
    output_description: str
    inputs: Inputs
    outputs: Outputs
