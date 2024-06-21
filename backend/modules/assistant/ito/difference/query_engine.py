import asyncio
import math
import os
import pickle
from enum import Enum
from typing import List, Optional

import nest_asyncio
import uvloop
from langchain_core.pydantic_v1 import BaseModel, Field
from llama_index.core import Document, QueryBundle, VectorStoreIndex
from llama_index.core.node_parser import MarkdownNodeParser
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.schema import BaseNode, MetadataMode, NodeWithScore
from llama_index.llms.openai import OpenAI
from llama_index.postprocessor.cohere_rerank import CohereRerank


class DecisionEnum(str, Enum):
    authorized = "Authorized"
    to_avoid = "To Avoid"
    forbidden = "Forbidden"


class Ingredient(BaseModel):
    """Represents an ingredient and its associated decision."""

    name: str = Field(description="Name of the ingredient")
    detailed_answer: str = Field(description="Detailed answer with explanations")
    decision: DecisionEnum = Field(
        description="Decision made: authorized / to avoid / forbidden"
    )
    used_chunks: list[int] = Field(
        description="List of chunks id used to generate the answer, None if the response was not found in the chunks. -  focus on those with high information density that directly answer the query. Never select a table of content or any text similar."
    )
    # more_info: str = Field(description="More information on how the chunks (with ID) were used to generate the answer, start with look into chunk id to ..., then look into chunk id ..., keep it short")


class AddChunkId(BaseNodePostprocessor):
    def _postprocess_nodes(  # type: ignore
        self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle]
    ) -> List[NodeWithScore]:
        for i, n in enumerate(nodes):
            content = n.node.get_content()
            n.node.set_content(f"Chunk #{i} : \n {content}")
        return nodes


class GeneticRerank(BaseNodePostprocessor):
    # top_n: int = Field(description="Top N nodes to return.")
    def _postprocess_nodes(  # type: ignore
        self, nodes: List[NodeWithScore], query_bundle: Optional[QueryBundle]
    ) -> List[NodeWithScore]:  # type: ignore
        retrieved_nodes = {}
        for n in nodes:
            if n.score is None:
                n.score = 0.0
            n.score += math.tanh(0.05 * float(n.node.metadata["info_density"]))
            retrieved_nodes[n.node.id_] = n.score

        # sort nodes by score
        sorted_ids = sorted(
            retrieved_nodes, key=lambda n: retrieved_nodes[n], reverse=True
        )

        # return a list of topk nodes retrieve by id
        sorted_nodes = [node for node in nodes if node.node.id_ in sorted_ids[:5]]
        # return a list of topk nodes
        return sorted_nodes
        # return nodes


class DiffQueryEngine:
    def __init__(self, source_md: List[str], top_k: int = 15):
        self.cleaned_nodes: List[BaseNode] | None = None
        self.query_engine = None
        self.top_k = top_k
        self.get_query_engine(source_md)

    def get_query_engine(self, source_md: List[str]) -> None:
        """Get a query engine for markdown files."""
        if not isinstance(asyncio.get_event_loop(), uvloop.Loop):
            nest_asyncio.apply()

        md_document = [Document(text=sub_source_md) for sub_source_md in source_md]
        node_parser = MarkdownNodeParser()

        if not os.path.exists("./charte.pkl"):
            raw_nodes = node_parser.get_nodes_from_documents(
                md_document, show_progress=False
            )
            self.cleaned_nodes = [
                node
                for node in raw_nodes
                if node.get_content(metadata_mode=MetadataMode.EMBED) != ""
            ]
            for node in self.cleaned_nodes:
                node.metadata["info_density"] = 0

            pickle.dump(self.cleaned_nodes, open("./charte.pkl", "wb"))
        else:
            self.cleaned_nodes = pickle.load(open("./charte.pkl", "rb"))

        if not self.cleaned_nodes:
            raise ValueError("No nodes found in the document.")

        # FIXME: Delete this line once nodes saved :
        for node in self.cleaned_nodes:
            node.metadata["info_density"] = 0

        llm = OpenAI(model="gpt-4o", temperature=0.0)  # 0.1

        vector_index = VectorStoreIndex(self.cleaned_nodes)
        # vector_retriever = vector_index.as_retriever(similarity_top_k=top_k, outpuy_cls = Ingredient)

        # query_engine = RetrieverQueryEngine.from_args(vector_retriever)
        self.query_engine = vector_index.as_query_engine(
            output_cls=Ingredient,
            similarity_top_k=self.top_k,
            llm=llm,
            node_postprocessors=[CohereRerank(top_n=10), GeneticRerank(), AddChunkId()],
            response_mode="tree_summarize",
        )

    def update_query_engine(self, modified_nodes: List[BaseNode]) -> None:
        """Update the query engine with modified nodes."""

        if not self.cleaned_nodes:
            raise ValueError("No nodes found in the document.")
        modified_nodes_ids = [node.id_ for node in modified_nodes]

        for node in self.cleaned_nodes:
            if node.id_ in modified_nodes_ids:
                print("Node found")
                node.metadata["info_density"] += 1

        vector_index = VectorStoreIndex(self.cleaned_nodes)
        self.query_engine = vector_index.as_query_engine(
            output_cls=Ingredient,
            similarity_top_k=self.top_k,
            llm=OpenAI(model="gpt-4o", temperature=0.0),
            node_postprocessors=[CohereRerank(top_n=10), GeneticRerank(), AddChunkId()],
            response_mode="tree_summarize",
        )
