import hashlib
import mimetypes
import os
import warnings
from contextlib import asynccontextmanager
from enum import Enum
from pathlib import Path
from typing import Any, AsyncGenerator, AsyncIterable, Self
from uuid import UUID, uuid4

import aiofiles
from openai import BaseModel


class QuivrFileSerialized(BaseModel):
    id: UUID
    brain_id: UUID
    path: Path
    original_filename: str
    file_size: int | None
    file_extension: str
    file_sha1: str
    additional_metadata: dict[str, Any]


class FileExtension(str, Enum):
    txt = ".txt"
    pdf = ".pdf"
    csv = ".csv"
    doc = ".doc"
    docx = ".docx"
    pptx = ".pptx"
    xls = ".xls"
    xlsx = ".xlsx"
    md = ".md"
    mdx = ".mdx"
    markdown = ".markdown"
    bib = ".bib"
    epub = ".epub"
    html = ".html"
    odt = ".odt"
    py = ".py"
    ipynb = ".ipynb"
    m4a = ".m4a"
    mp3 = ".mp3"
    webm = ".webm"
    mp4 = ".mp4"
    mpga = ".mpga"
    wav = ".wav"
    mpeg = ".mpeg"


def get_file_extension(file_path: Path) -> FileExtension | str:
    try:
        mime_type, _ = mimetypes.guess_type(file_path.name)
        if mime_type:
            mime_ext = mimetypes.guess_extension(mime_type)
            if mime_ext:
                return FileExtension(mime_ext)
        return FileExtension(file_path.suffix)
    except ValueError:
        warnings.warn(
            f"File {file_path.name} extension isn't recognized. Make sure you have registered a parser for {file_path.suffix}",
            stacklevel=2,
        )
        return file_path.suffix


async def load_qfile(brain_id: UUID, path: str | Path):
    if not isinstance(path, Path):
        path = Path(path)

    if not path.exists():
        raise FileExistsError(f"file {path} doesn't exist")

    file_size = os.stat(path).st_size

    async with aiofiles.open(path, mode="rb") as f:
        file_sha1 = hashlib.sha1(await f.read()).hexdigest()

    try:
        # NOTE: when loading from existing storage, file name will be uuid
        id = UUID(path.name)
    except ValueError:
        id = uuid4()

    return QuivrFile(
        id=id,
        brain_id=brain_id,
        path=path,
        original_filename=path.name,
        file_extension=get_file_extension(path),
        file_size=file_size,
        file_sha1=file_sha1,
    )


class QuivrFile:
    __slots__ = [
        "id",
        "brain_id",
        "path",
        "original_filename",
        "file_size",
        "file_extension",
        "file_sha1",
        "additional_metadata",
    ]

    def __init__(
        self,
        id: UUID,
        original_filename: str,
        path: Path,
        brain_id: UUID,
        file_sha1: str,
        file_extension: FileExtension | str,
        file_size: int | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.id = id
        self.brain_id = brain_id
        self.path = path
        self.original_filename = original_filename
        self.file_size = file_size
        self.file_extension = file_extension
        self.file_sha1 = file_sha1
        self.additional_metadata = metadata if metadata else {}

    def __repr__(self) -> str:
        return f"QuivrFile-{self.id} original_filename:{self.original_filename}"

    @asynccontextmanager
    async def open(self) -> AsyncGenerator[AsyncIterable[bytes], None]:
        # TODO(@aminediro) : match on path type
        f = await aiofiles.open(self.path, mode="rb")
        try:
            yield f
        finally:
            await f.close()

    @property
    def metadata(self) -> dict[str, Any]:
        return {
            "qfile_id": self.id,
            "qfile_path": self.path,
            "original_file_name": self.original_filename,
            "file_sha1": self.file_sha1,
            "file_size": self.file_size,
            **self.additional_metadata,
        }

    def serialize(self) -> QuivrFileSerialized:
        return QuivrFileSerialized(
            id=self.id,
            brain_id=self.brain_id,
            path=self.path.absolute(),
            original_filename=self.original_filename,
            file_size=self.file_size,
            file_extension=self.file_extension,
            file_sha1=self.file_sha1,
            additional_metadata=self.additional_metadata,
        )

    @classmethod
    def deserialize(cls, serialized: QuivrFileSerialized) -> Self:
        return cls(
            id=serialized.id,
            brain_id=serialized.brain_id,
            path=serialized.path,
            original_filename=serialized.original_filename,
            file_size=serialized.file_size,
            file_extension=serialized.file_extension,
            file_sha1=serialized.file_sha1,
            metadata=serialized.additional_metadata,
        )
