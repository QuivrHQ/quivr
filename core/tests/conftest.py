import json
import os
from pathlib import Path
from typing import Any, List, Type
from uuid import uuid4
from unittest.mock import Mock

import pytest
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.language_models import FakeListChatModel
from langchain_core.messages.ai import AIMessageChunk
from pydantic import BaseModel
from langchain_core.runnables.utils import AddableDict
from langchain_core.vectorstores import InMemoryVectorStore
from quivr_core.rag.entities.config import LLMEndpointConfig
from quivr_core.files.file import FileExtension, QuivrFile
from quivr_core.llm import LLMEndpoint


class FakeLLMWithStructuredOutputWrapper:
    """
    A wrapper around FakeListChatModel to add with_structured_output
    without modifying the Pydantic model instance directly.
    """

    def __init__(self, llm: FakeListChatModel):
        self._llm = llm

    def with_structured_output(self, schema: Type[BaseModel], **kwargs: Any) -> Any:
        """Mock the with_structured_output method."""
        # This mock should ideally return an object that can be invoked/ainvoked
        # and produces an instance of `schema`.
        # For simplicity, we'll return a mock that itself can be called.
        structured_llm_mock = Mock()
        # Simulate that invoking this would return an instance of the schema
        # For a generic mock, we can have it return a new Mock instance
        structured_llm_mock.invoke = Mock(return_value=Mock(spec=schema))
        structured_llm_mock.ainvoke = Mock(return_value=Mock(spec=schema))
        return structured_llm_mock

    def __getattr__(self, name: str) -> Any:
        """Delegate other attribute access to the wrapped LLM."""
        return getattr(self._llm, name)


@pytest.fixture(scope="function")
def temp_data_file(tmp_path):
    data = "This is some test data."
    temp_file = tmp_path / "data.txt"
    temp_file.write_text(data)
    return temp_file


@pytest.fixture(scope="function")
def quivr_txt(temp_data_file):
    return QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename=temp_data_file.name,
        path=temp_data_file,
        file_extension=FileExtension.txt,
        file_sha1="123",
    )


@pytest.fixture
def quivr_pdf():
    return QuivrFile(
        id=uuid4(),
        brain_id=uuid4(),
        original_filename="dummy.pdf",
        path=Path("./tests/processor/data/dummy.pdf"),
        file_extension=FileExtension.pdf,
        file_sha1="13bh234jh234",
    )


@pytest.fixture
def full_response():
    return "Natural Language Processing (NLP) is a field of artificial intelligence that focuses on the interaction between computers and humans through natural language. The ultimate objective of NLP is to enable computers to understand, interpret, and respond to human language in a way that is both valuable and meaningful. NLP combines computational linguistics—rule-based modeling of human language—with statistical, machine learning, and deep learning models. This combination allows computers to process human language in the form of text or voice data and to understand its full meaning, complete with the speaker or writer's intent and sentiment. Key tasks in NLP include text and speech recognition, translation, sentiment analysis, and topic segmentation."


@pytest.fixture
def chunks_stream_answer():
    with open("./tests/chunk_stream_fixture.jsonl", "r") as f:
        raw_chunks = list(f)

    chunks = []
    for rc in raw_chunks:
        chunk = AddableDict(**json.loads(rc))
        if "answer" in chunk:
            chunk["answer"] = AIMessageChunk(**chunk["answer"])
            chunks.append(chunk)
    return chunks


@pytest.fixture(autouse=True)
def openai_api_key():
    os.environ["OPENAI_API_KEY"] = "this-is-a-test-key"


@pytest.fixture
def answers():
    return [f"answer_{i}" for i in range(10)]


@pytest.fixture(scope="function")
def fake_llm(answers: List[str]):
    original_llm = FakeListChatModel(responses=answers)
    # Wrap the original LLM with our custom wrapper
    wrapped_llm = FakeLLMWithStructuredOutputWrapper(original_llm)
    return LLMEndpoint(
        llm=wrapped_llm, llm_config=LLMEndpointConfig(model="fake_model")
    )


@pytest.fixture(scope="function")
def embedder():
    return DeterministicFakeEmbedding(size=20)


@pytest.fixture(scope="function")
def mem_vector_store(embedder):
    return InMemoryVectorStore(embedder)
