from typing import List
from uuid import UUID
from pydantic import BaseModel
from datetime import date

class BrainUsage(BaseModel):
    date: date
    usage_count: int

class BrainUsages(BaseModel):
    brain_id: UUID
    usages: List[BrainUsage]

class BrainsUsage(BaseModel):
    brains_usage: List[BrainUsages]