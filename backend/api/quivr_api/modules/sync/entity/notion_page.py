from datetime import datetime
from typing import Any, List, Literal, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

from quivr_api.modules.sync.entity.sync_models import NotionSyncFile


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
    emoji: str


class ExternalCoverData(BaseModel):
    url: str


class Cover(BaseModel):
    type: Literal["external"]
    external: ExternalCoverData


class PageParent(BaseModel):
    type: Literal["page_id"]
    page_id: UUID


class BlockParent(BaseModel):
    type: Literal["block_id"]
    block_id: UUID


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
    title: Title | None = None


class NotionPage(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: UUID
    created_time: datetime
    last_edited_time: datetime
    url: str
    archived: bool
    in_trash: bool | None
    public_url: str | None
    parent: Union[PageParent, DatabaseParent, WorkspaceParent, BlockParent] = Field(
        discriminator="type"
    )
    cover: Cover | None
    icon: Icon | None
    properties: PageProps
    sync_user_id: UUID | None = Field(default=None, foreign_key="syncs_user.id")  # type: ignore

    # TODO: Fix  UUID in table NOTION
    def _get_parent_id(self) -> UUID | None:
        match self.parent:
            case PageParent(page_id=page_id):
                return page_id
            case DatabaseParent():
                return None
            case WorkspaceParent():
                return None
            case BlockParent():
                return None

    def to_syncfile(self, user_id: UUID, sync_user_id: int) -> NotionSyncFile:
        name = (
            self.properties.title.title[0].text.content if self.properties.title else ""
        )
        return NotionSyncFile(
            notion_id=self.id,  # TODO: store as UUID
            parent_id=self._get_parent_id(),
            name=f"{name}.md",
            icon=self.icon.emoji if self.icon else "",
            mime_type="md",
            web_view_link=self.url,
            is_folder=True,
            last_modified=self.last_edited_time,
            type="page",
            user_id=user_id,
            sync_user_id=sync_user_id,
        )


class NotionSearchResult(BaseModel):
    model_config = ConfigDict(extra="allow")
    results: list[NotionPage]
    has_more: bool
    next_cursor: str | None
