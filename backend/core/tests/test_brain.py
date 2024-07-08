import pytest
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.language_models import FakeListChatModel

from quivr_core.brain import Brain


@pytest.fixture
def temp_data_file(tmpdir):
    data = "This is some test data."
    temp_file = tmpdir.join("data.txt")
    temp_file.write(data)
    return temp_file


@pytest.fixture
def answers():
    return [f"answer_{i}" for i in range(10)]


@pytest.fixture(scope="function")
def llm(answers: list[str]):
    return FakeListChatModel(responses=answers)


@pytest.fixture(scope="function")
def embedder():
    return DeterministicFakeEmbedding(size=20)


def test_brain_from_files_exception():
    # Testing no files
    with pytest.raises(ValueError):
        Brain.from_files(name="test_brain", file_paths=[])


def test_brain_ask_txt(llm, embedder, temp_data_file, answers):
    brain = Brain.from_files(
        name="test_brain", file_paths=[temp_data_file], embedder=embedder, llm=llm
    )

    assert brain.llm == llm
    assert brain.vector_db.embeddings == embedder

    answer = brain.ask("question")

    assert answer.answer == answers[0]
    assert answer.metadata == answers[0]
