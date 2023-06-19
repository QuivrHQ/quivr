from typing import List, Optional, Tuple
from uuid import UUID

from pydantic import BaseModel


class Brain(BaseModel):
    brain_id: Optional[UUID] = None
    brain_name: str = "New Brain"
    status: str = "public"
    model: str = "gpt-3.5-turbo-0613"
    temperature: float = 0.0
    max_tokens: int = 256
    
class BrainToUpdate(BaseModel): 
    brain_id: UUID
    brain_name: Optional[str] = "New Brain"
    status: Optional[str] = "public"
    model: Optional[str] = "gpt-3.5-turbo-0613"
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 256
    file_sha1: Optional[str] = ''