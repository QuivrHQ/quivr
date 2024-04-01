from typing import List
from uuid import UUID
from pydantic import BaseModel
from datetime import date

class Usage(BaseModel):
    date: date
    usage_count: int

class BrainUsages(BaseModel):
    brain_id: UUID
    usages: List[Usage]

class BrainsUsages(BaseModel):
    brains_usages: List[BrainUsages]