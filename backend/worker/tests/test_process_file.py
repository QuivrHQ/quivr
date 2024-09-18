import datetime
import os
from pathlib import Path
from uuid import uuid4

import pytest
from quivr_api.modules.brain.entity.brain_entity import BrainEntity, BrainType
from quivr_core.files.file import FileExtension
from quivr_worker.files import File, build_file
from quivr_worker.parsers.crawler import URL, slugify
from quivr_worker.process.process_file import parse_file


def test_build_file():
    random_bytes = os.urandom(128)
    brain_id = uuid4()
    file_name = f"{brain_id}/test_file.txt"
    knowledge_id = uuid4()

    with build_file(random_bytes, knowledge_id, file_name) as file:
        assert file.file_size == 128
        assert file.file_name == "test_file.txt"
        assert file.id == knowledge_id
        assert file.file_extension == FileExtension.txt


def test_build_url():
    random_bytes = os.urandom(128)
    crawl_website = URL(url="http://url.url")
    file_name = slugify(crawl_website.url) + ".txt"
    knowledge_id = uuid4()

    with build_file(
        random_bytes,
        knowledge_id,
        file_name=file_name,
        original_file_name=crawl_website.url,
    ) as file:
        qfile = file.to_qfile(brain_id=uuid4())
        assert qfile.metadata["original_file_name"] == crawl_website.url
        assert qfile.metadata["file_name"] == file_name


@pytest.mark.asyncio
async def test_parse_audio(monkeypatch, audio_file):
    from openai.resources.audio.transcriptions import Transcriptions
    from openai.types.audio.transcription import Transcription

    def transcribe(*args, **kwargs):
        return Transcription(text="audio data")

    monkeypatch.setattr(Transcriptions, "create", transcribe)
    brain = BrainEntity(
        brain_id=uuid4(),
        name="test",
        brain_type=BrainType.doc,
        last_update=datetime.datetime.now(),
    )
    chunks = await parse_file(
        file=audio_file,
        brain=brain,
    )
    assert len(chunks) > 0
    assert chunks[0].page_content == "audio data"


@pytest.mark.asyncio
async def test_parse_file(file_instance):
    brain = BrainEntity(
        brain_id=uuid4(),
        name="test",
        brain_type=BrainType.doc,
        last_update=datetime.datetime.now(),
    )
    chunks = await parse_file(
        file=file_instance,
        brain=brain,
    )
    assert len(chunks) > 0


@pytest.mark.asyncio
async def test_parse_file_pdf():
    file_instance = File(
        knowledge_id=uuid4(),
        file_sha1="124",
        file_extension=".pdf",
        file_name="test",
        original_file_name="test",
        file_size=1000,
        tmp_file_path=Path("./tests/sample.pdf"),
    )
    brain = BrainEntity(
        brain_id=uuid4(),
        name="test",
        brain_type=BrainType.doc,
        last_update=datetime.datetime.now(),
    )
    chunks = await parse_file(
        file=file_instance,
        brain=brain,
    )

    assert len(chunks[0].page_content) > 0
    assert len(chunks) > 0
