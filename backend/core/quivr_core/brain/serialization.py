from pathlib import Path
from typing import Any, Dict, Literal, Union
from uuid import UUID

from pydantic import BaseModel, Field, SecretStr

from quivr_core.config import LLMEndpointConfig
from quivr_core.files.file import QuivrFileSerialized
from quivr_core.models import ChatMessage


class EmbedderConfig(BaseModel):
    embedder_type: Literal["openai_embedding"] = "openai_embedding"
    # TODO: type this correctly
    config: Dict[str, Any]


class PGVectorConfig(BaseModel):
    vectordb_type: Literal["pgvector"] = "pgvector"
    pg_url: str
    pg_user: str
    pg_psswd: SecretStr
    table_name: str
    vector_dim: int


class FAISSConfig(BaseModel):
    vectordb_type: Literal["faiss"] = "faiss"
    vectordb_folder_path: str


class LocalStorageConfig(BaseModel):
    storage_type: Literal["local_storage"] = "local_storage"
    storage_path: Path
    files: dict[UUID, QuivrFileSerialized]


class TransparentStorageConfig(BaseModel):
    storage_type: Literal["transparent_storage"] = "transparent_storage"
    files: dict[UUID, QuivrFileSerialized]


class BrainSerialized(BaseModel):
    id: UUID
    name: str
    chat_history: list[ChatMessage]
    vectordb_config: Union[FAISSConfig, PGVectorConfig] = Field(
        ..., discriminator="vectordb_type"
    )
    storage_config: Union[TransparentStorageConfig, LocalStorageConfig] = Field(
        ..., discriminator="storage_type"
    )

    llm_config: LLMEndpointConfig
    embedding_config: EmbedderConfig
