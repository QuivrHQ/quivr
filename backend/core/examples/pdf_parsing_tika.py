from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.language_models import FakeListChatModel

from quivr_core import Brain
from quivr_core.config import LLMEndpointConfig
from quivr_core.llm.llm_endpoint import LLMEndpoint
from quivr_core.processor.tika_processor import TikaProcessor

if __name__ == "__main__":
    pdf_paths = ["../tests/processor/data/dummy.pdf"]
    brain = Brain.from_files(
        name="test_brain",
        file_paths=[],
        llm=LLMEndpoint(
            llm=FakeListChatModel(responses=["good"]),
            llm_config=LLMEndpointConfig(model="fake_model"),
        ),
        embedder=DeterministicFakeEmbedding(size=20),
        processors_mapping={
            ".pdf": TikaProcessor(),
        },
    )
