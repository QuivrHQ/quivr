from typing import List
from pydantic import BaseModel
from datetime import date

class Usage(BaseModel):
    date: date
    usage_count: int

class BrainsUsages(BaseModel):
    usages: List[Usage]