import os
from uuid import uuid4

import pytest
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_worker.process.process_file import parse_qfile
from quivr_worker.process.utils import build_qfile


def test_build_qfile_fail(local_knowledge_file: KnowledgeDB):
    random_bytes = os.urandom(128)
    local_knowledge_file.file_sha1 = None
    with pytest.raises(AssertionError):
        with build_qfile(knowledge=local_knowledge_file, file_data=random_bytes) as _:
            pass
    local_knowledge_file.file_sha1 = "sha1"
    local_knowledge_file.id = None
    with pytest.raises(AssertionError):
        with build_qfile(knowledge=local_knowledge_file, file_data=random_bytes) as _:
            pass

    local_knowledge_file.id = uuid4()
    local_knowledge_file.file_name = None
    with pytest.raises(AssertionError):
        with build_qfile(knowledge=local_knowledge_file, file_data=random_bytes) as _:
            pass


def test_build_qfile(local_knowledge_file: KnowledgeDB):
    random_bytes = os.urandom(128)
    local_knowledge_file.file_sha1 = "sha1"

    with build_qfile(knowledge=local_knowledge_file, file_data=random_bytes) as file:
        assert file.id == local_knowledge_file.id
        assert file.file_size == 128
        assert file.original_filename == local_knowledge_file.file_name
        assert file.file_extension == local_knowledge_file.extension
        if local_knowledge_file.metadata_:
            assert local_knowledge_file.metadata_.items() <= file.metadata.items()
        assert file.brain_id is None


@pytest.mark.asyncio(loop_scope="session")
async def test_parse_audio(monkeypatch, audio_qfile):
    from openai.resources.audio.transcriptions import Transcriptions
    from openai.types.audio.transcription import Transcription

    def transcribe(*args, **kwargs):
        return Transcription(text="audio data")

    monkeypatch.setattr(Transcriptions, "create", transcribe)
    chunks = await parse_qfile(
        qfile=audio_qfile,
    )
    assert len(chunks) > 0
    assert chunks[0].page_content == "audio data"


@pytest.mark.asyncio(loop_scope="session")
async def test_parse_file(qfile_instance):
    chunks = await parse_qfile(
        qfile=qfile_instance,
    )
    assert len(chunks) > 0


@pytest.mark.asyncio(loop_scope="session")
async def test_parse_file_pdf(pdf_qfile):
    chunks = await parse_qfile(
        qfile=pdf_qfile,
    )
    assert len(chunks[0].page_content) > 0
    assert len(chunks) > 0
