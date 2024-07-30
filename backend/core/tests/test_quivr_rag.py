from uuid import uuid4

import pytest
from quivr_core.chat import ChatHistory
from quivr_core.config import LLMEndpointConfig, RAGConfig
from quivr_core.llm import LLMEndpoint
from quivr_core.models import ParsedRAGChunkResponse, RAGResponseMetadata
from quivr_core.quivr_rag import QuivrQARAG


@pytest.fixture(scope="function")
def mock_chain_qa_stream(monkeypatch, chunks_stream_answer):
    class MockQAChain:
        async def astream(self, *args, **kwargs):
            for c in chunks_stream_answer:
                yield c

    def mock_qa_chain(*args, **kwargs):
        return MockQAChain()

    monkeypatch.setattr(QuivrQARAG, "build_chain", mock_qa_chain)


@pytest.mark.base
@pytest.mark.asyncio
async def test_quivrqarag(
    mem_vector_store, full_response, mock_chain_qa_stream, openai_api_key
):
    # Making sure the model
    llm_config = LLMEndpointConfig(model="gpt-4o")
    llm = LLMEndpoint.from_config(llm_config)
    rag_config = RAGConfig(llm_config=llm_config)
    chat_history = ChatHistory(uuid4(), uuid4())
    rag_pipeline = QuivrQARAG(
        rag_config=rag_config, llm=llm, vector_store=mem_vector_store
    )

    stream_responses: list[ParsedRAGChunkResponse] = []

    # Making sure that we are calling the func_calling code path
    assert rag_pipeline.llm_endpoint.supports_func_calling()
    async for resp in rag_pipeline.answer_astream(
        "answer in bullet points. tell me something", chat_history, []
    ):
        stream_responses.append(resp)

    assert all(
        not r.last_chunk for r in stream_responses[:-1]
    ), "Some chunks before last have last_chunk=True"
    assert stream_responses[-1].last_chunk

    for idx, response in enumerate(stream_responses[1:-1]):
        assert (
            len(response.answer) > 0
        ), f"Sent an empty answer {response} at index {idx+1}"

    # Verify metadata
    default_metadata = RAGResponseMetadata().model_dump()
    assert all(
        r.metadata.model_dump() == default_metadata for r in stream_responses[:-1]
    )
    last_response = stream_responses[-1]
    # TODO(@aminediro) : test responses with sources
    assert last_response.metadata.sources == []
    assert last_response.metadata.citations == []

    # Assert whole response makes sense
    assert "".join([r.answer for r in stream_responses]) == full_response
