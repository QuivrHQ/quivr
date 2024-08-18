from datetime import datetime
from typing import Any, List, Literal, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TextContent(BaseModel):
    content: str | None
    link: str | None


class TitleItem(BaseModel):
    type: Literal["text"]
    text: TextContent
    annotations: dict[str, Any]
    plain_text: str


class Title(BaseModel):
    id: str
    type: Literal["title"]
    title: List[TitleItem]


class StatusData(BaseModel):
    id: UUID
    name: str
    color: str


class Status(BaseModel):
    id: str
    type: Literal["status"]
    status: StatusData


class Icon(BaseModel):
    type: Literal["emoji"]
    emoji: str | None


class ExternalCoverData(BaseModel):
    url: str


class Cover(BaseModel):
    type: Literal["external"]
    external: ExternalCoverData


class PageParent(BaseModel):
    type: Literal["parent_id"]
    page_id: UUID


class DatabaseParent(BaseModel):
    type: Literal["database_id"]
    database_id: UUID


class WorkspaceParent(BaseModel):
    type: Literal["workspace"]
    workspace: bool = True

    @field_validator("workspace")
    @classmethod
    def workspace_always_true(cls, w: bool) -> bool:
        assert w, "workspace value always True"
        return w


class PageProps(BaseModel):
    title: Title | None = Field(alias="Title")
    status: Status | None = Field(alias="Status")


class NotionPage(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: UUID
    created_time: datetime
    last_edited_time: datetime
    archived: bool
    in_trash: bool
    url: str
    public_url: str
    parent: Union[PageParent, DatabaseParent, WorkspaceParent] = Field(
        discriminator="type"
    )
    cover: Cover | None
    icon: Icon | None
    properties: PageProps
