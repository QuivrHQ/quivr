# Brain

The brain is the essential component of Quivr that stores and processes the knowledge you want to retrieve informations from. Simply create a brain with the files you want to process and use the latest Quivr RAG workflow to retrieve informations from the knowledge.

Quick Start 🪄:

```python
from quivr_core import Brain
from quivr_core.quivr_rag_langgraph import QuivrQARAGLangGraph


brain = Brain.from_files(name="My Brain", file_paths=["file1.pdf", "file2.pdf"])
answer = brain.ask("What is Quivr ?")
print("Answer Quivr :", answer.answer)

```

Pimp your Brain 🔨 :

```python
from quivr_core import Brain
from quivr_core.llm.llm_endpoint import LLMEndpoint
from quivr_core.embedder.embedder import DeterministicFakeEmbedding
from quivr_core.llm.llm_endpoint import LLMEndpointConfig
from quivr_core.llm.llm_endpoint import FakeListChatModel

brain = Brain.from_files(
        name="test_brain",
        file_paths=["my/information/source/file.pdf"],
        llm=LLMEndpoint(
            llm=FakeListChatModel(responses=["good"]),
            llm_config=LLMEndpointConfig(model="fake_model", llm_base_url="local"),
        ),
        embedder=DeterministicFakeEmbedding(size=20),
    )

answer = brain.ask(
            "What is Quivr ?"
        )
print("Answer Quivr :", answer.answer)

```
