from enum import IntEnum
from typing import List
from pydantic import BaseModel
from datetime import date

class Range(IntEnum):
    WEEK = 7
    MONTH = 30
    QUARTER = 90

class Usage(BaseModel):
    date: date
    usage_count: int

class BrainsUsages(BaseModel):
    usages: List[Usage]