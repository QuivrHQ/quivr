from typing import Any, List, Optional

from pydantic import BaseModel


class AssistantFileRequirement(BaseModel):
    name: str
    description: Optional[str] = None
    required: bool = True
    accepted_types: Optional[List[str]] = None  # e.g., ['text/csv', 'application/json']


class AssistantInput(BaseModel):
    name: str
    description: str
    type: str  # e.g., 'boolean', 'uuid', 'string'
    required: bool = True
    regex: Optional[str] = None
    options: Optional[List[Any]] = None  # For predefined choices
    default: Optional[Any] = None


class AssistantSettings(BaseModel):
    inputs: List[AssistantInput]
    files: Optional[List[AssistantFileRequirement]] = None


class Assistant(BaseModel):
    id: int
    name: str
    description: str
    settings: AssistantSettings
    required_files: Optional[List[str]] = None  # List of required file names
