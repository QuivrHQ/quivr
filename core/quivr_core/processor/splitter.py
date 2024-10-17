from pydantic import BaseModel


class SplitterConfig(BaseModel):
    """
    This class is used to configure the chunking of the documents.

    Chunk size is the number of characters in the chunk.
    Chunk overlap is the number of characters that the chunk will overlap with the previous chunk.
    """

    chunk_size: int = 400
    chunk_overlap: int = 100
