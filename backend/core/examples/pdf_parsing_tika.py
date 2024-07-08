from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.language_models import FakeListChatModel

from quivr_core import Brain
from quivr_core.processor.default_parsers import DEFAULT_PARSERS
from quivr_core.processor.pdf_processor import TikaParser

if __name__ == "__main__":
    pdf_paths = ["../tests/processor/data/dummy.pdf"]
    brain = Brain.from_files(
        name="test_brain",
        file_paths=[],
        llm=FakeListChatModel(responses=["good"]),
        embedder=DeterministicFakeEmbedding(size=20),
        processors_mapping={
            **DEFAULT_PARSERS,
            ".pdf": TikaParser(),
        },
    )
