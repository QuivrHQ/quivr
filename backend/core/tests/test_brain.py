from uuid import uuid4

import pytest
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding, Embeddings
from langchain_core.language_models import FakeListChatModel

from quivr_core.brain import Brain
from quivr_core.config import LLMEndpointConfig
from quivr_core.llm import LLMEndpoint
from quivr_core.storage.local_storage import TransparentStorage


@pytest.fixture(scope="function")
def temp_data_file(tmp_path):
    data = "This is some test data."
    temp_file = tmp_path / "data.txt"
    temp_file.write_text(data)
    return temp_file


@pytest.fixture
def answers():
    return [f"answer_{i}" for i in range(10)]


@pytest.fixture(scope="function")
def llm(answers: list[str]):
    llm = FakeListChatModel(responses=answers)
    return LLMEndpoint(llm=llm, llm_config=LLMEndpointConfig(model="fake_model"))


@pytest.fixture(scope="function")
def embedder():
    return DeterministicFakeEmbedding(size=20)


def test_brain_empty_files():
    # Testing no files
    with pytest.raises(ValueError):
        Brain.from_files(name="test_brain", file_paths=[])


def test_brain_from_files_success(llm: LLMEndpoint, embedder, temp_data_file):
    brain = Brain.from_files(
        name="test_brain", file_paths=[temp_data_file], embedder=embedder, llm=llm
    )
    assert brain.name == "test_brain"
    assert brain.chat_history == []
    assert brain.llm == llm
    assert brain.vector_db.embeddings == embedder
    # storage
    assert isinstance(brain.storage, TransparentStorage)
    assert len(brain.storage.get_files()) == 1


@pytest.mark.asyncio
async def test_brain_ask_txt(llm: LLMEndpoint, embedder, temp_data_file, answers):
    brain = await Brain.afrom_files(
        name="test_brain", file_paths=[temp_data_file], embedder=embedder, llm=llm
    )
    answer = brain.ask("question")

    assert answer.answer == answers[1]
    assert answer.metadata is not None
    assert answer.metadata.sources is not None
    assert answer.metadata.sources[0].metadata["source"] == str(temp_data_file)


@pytest.mark.asyncio
async def test_brain_from_langchain_docs(llm, embedder):
    chunk = Document("content_1", metadata={"id": uuid4()})
    brain = await Brain.afrom_langchain_documents(
        name="test", langchain_documents=[chunk], embedder=embedder
    )
    # No appended files
    assert len(brain.storage.get_files()) == 0
    assert len(brain.chat_history) == 0


@pytest.mark.asyncio
async def test_brain_search(
    embedder: Embeddings,
):
    chunk = Document("content_1", metadata={"id": uuid4()})
    brain = await Brain.afrom_langchain_documents(
        name="test", langchain_documents=[chunk], embedder=embedder
    )

    result = await brain.asearch("content_1")

    assert len(result) == 1
    assert result[0].chunk == chunk
    assert result[0].score == 0
