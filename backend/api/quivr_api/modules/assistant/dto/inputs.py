
from pydantic import BaseModel

class CreateTask(BaseModel):
    pretty_id: str