from uuid import UUID

from pydantic import BaseModel

# class FileInStorage(BaseModel):
#     id: Optional[UUID] = None
#     knowledge_id: Optional[UUID] = None
#     owner_id: Optional[UUID] = None
#     file_to_upload: Optional[UploadFile] = None
#     data: Optional[bytes] = None
#     name: Optional[str] = None
#     size: Optional[int] = None
#     extension: Optional[str] = None


class FileInStorage(BaseModel):
    Id: UUID
    Key: str

    @property
    def id(self) -> UUID:
        return self.Id

    @property
    def key(self) -> str:
        return self.Key
