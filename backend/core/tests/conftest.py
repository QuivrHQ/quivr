import os

import pytest
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.language_models import FakeListChatModel
from langchain_core.vectorstores import InMemoryVectorStore

from quivr_core.config import LLMEndpointConfig
from quivr_core.llm import LLMEndpoint


@pytest.fixture(scope="session", autouse=True)
def openai_api_key():
    os.environ["OPENAI_API_KEY"] = "abcd"


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
def fake_llm(answers: list[str]):
    llm = FakeListChatModel(responses=answers)
    return LLMEndpoint(llm=llm, llm_config=LLMEndpointConfig(model="fake_model"))


@pytest.fixture(scope="function")
def embedder():
    return DeterministicFakeEmbedding(size=20)


@pytest.fixture(scope="function")
def mem_vector_store(embedder):
    return InMemoryVectorStore(embedder)
