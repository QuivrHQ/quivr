from uuid import UUID

from pydantic import BaseModel


class FileInStorage(BaseModel):
    Id: UUID
    Key: str

    @property
    def id(self) -> UUID:
        return self.Id

    @property
    def key(self) -> str:
        return self.Key
