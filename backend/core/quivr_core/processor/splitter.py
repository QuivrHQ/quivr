from pydantic import BaseModel


class SplitterConfig(BaseModel):
    chunk_size: int = 400
    chunk_overlap: int = 100
