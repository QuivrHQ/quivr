from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel
from quivr_api.modules.brain.entity.api_brain_definition_entity import (
    ApiBrainDefinitionEntity,
)
from quivr_api.modules.brain.entity.integration_brain import (
    IntegrationDescriptionEntity,
    IntegrationEntity,
)
from quivr_api.modules.prompt.entity.prompt import Prompt

# from sqlmodel import Enum as PGEnum
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlmodel import TIMESTAMP
from sqlmodel import UUID as PGUUID
from sqlmodel import Column, Field, Relationship, SQLModel, text


class BrainType(str, Enum):
    doc = "doc"
    api = "api"
    composite = "composite"
    integration = "integration"


class Brain(AsyncAttrs, SQLModel, table=True):
    __tablename__ = "brains"  # type: ignore

    brain_id: UUID | None = Field(
        default=None,
        sa_column=Column(
            PGUUID,
            server_default=text("uuid_generate_v4()"),
            primary_key=True,
        ),
    )
    name: str
    description: str
    status: str | None = None
    model: str | None = None
    max_tokens: int | None = None
    temperature: float | None = None
    last_update: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=False),
            server_default=text("CURRENT_TIMESTAMP"),
        ),
    )
    brain_type: BrainType | None = Field(
        sa_column=Column(
            PGEnum(BrainType, name="brain_type_enum", create_type=False),
            default=BrainType.integration,
        ),
    )
    brain_chat_history: List["ChatHistory"] = Relationship(  # noqa: F821
        back_populates="brain", sa_relationship_kwargs={"lazy": "select"}
    )
    prompt_id: UUID | None = Field(default=None, foreign_key="prompts.id")
    prompt: Prompt | None = Relationship(  # noqa: f821
        back_populates="brain", sa_relationship_kwargs={"lazy": "joined"}
    )

    # TODO : add
    # "meaning" "public"."vector",
    # "tags" "public"."tags"[]


class BrainEntity(BaseModel):
    brain_id: UUID
    name: str
    description: Optional[str] = None
    temperature: Optional[float] = None
    model: Optional[str] = None
    max_tokens: Optional[int] = None
    status: Optional[str] = None
    prompt_id: Optional[UUID] = None
    last_update: datetime
    brain_type: BrainType
    brain_definition: Optional[ApiBrainDefinitionEntity] = None
    connected_brains_ids: Optional[List[UUID]] = None
    raw: Optional[bool] = None
    jq_instructions: Optional[str] = None
    integration: Optional[IntegrationEntity] = None
    integration_description: Optional[IntegrationDescriptionEntity] = None

    @property
    def id(self) -> UUID:
        return self.brain_id

    def dict(self, **kwargs):
        data = super().dict(
            **kwargs,
        )
        data["id"] = self.id
        return data


class PublicBrain(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    number_of_subscribers: int = 0
    last_update: str
    brain_type: BrainType
    brain_definition: Optional[ApiBrainDefinitionEntity] = None


class RoleEnum(str, Enum):
    Viewer = "Viewer"
    Editor = "Editor"
    Owner = "Owner"


class BrainUser(BaseModel):
    id: UUID
    user_id: UUID
    rights: RoleEnum
    default_brain: bool = False


class MinimalUserBrainEntity(BaseModel):
    id: UUID
    name: str
    rights: RoleEnum
    status: str
    brain_type: BrainType
    description: str
    integration_logo_url: str
    max_files: int
