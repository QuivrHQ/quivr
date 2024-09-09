import asyncio
import json
from uuid import uuid4

from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.messages.ai import AIMessageChunk
from langchain_core.vectorstores import InMemoryVectorStore

from quivr_core.chat import ChatHistory
from quivr_core.config import LLMEndpointConfig, RAGConfig
from quivr_core.llm import LLMEndpoint
from quivr_core.quivr_rag import QuivrQARAG


async def main():
    rag_config = RAGConfig(llm_config=LLMEndpointConfig(model="gpt-4o"))
    embedder = DeterministicFakeEmbedding(size=20)
    vec = InMemoryVectorStore(embedder)

    llm = LLMEndpoint.from_config(rag_config.llm_config)
    chat_history = ChatHistory(uuid4(), uuid4())
    rag_pipeline = QuivrQARAG(rag_config=rag_config, llm=llm, vector_store=vec)

    conversational_qa_chain = rag_pipeline.build_chain("")

    with open("response.jsonl", "w") as f:
        async for chunk in conversational_qa_chain.astream(
            {
                "question": "What is NLP, give a very long detailed answer",
                "chat_history": chat_history,
                "custom_personality": None,
            },
            config={"metadata": {}},
        ):
            dict_chunk = {
                k: v.dict() if isinstance(v, AIMessageChunk) else v
                for k, v in chunk.items()
            }
            f.write(json.dumps(dict_chunk) + "\n")


asyncio.run(main())
