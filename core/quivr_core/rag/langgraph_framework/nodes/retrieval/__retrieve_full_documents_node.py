"""
Full document context retrieval node with runtime validation.
"""

import logging
from typing import Optional, Dict, Any
from collections import OrderedDict

from quivr_core.rag.entities.retriever import RetrieverConfig
from quivr_core.rag.langgraph_framework.base.node import (
    BaseNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from quivr_core.rag.langgraph_framework.task import UserTasks
from quivr_core.rag.langgraph_framework.base.extractors import ConfigExtractor
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig

logger = logging.getLogger("quivr_core")


class RetrieveFullDocumentsNode(BaseNode):
    """
    Node for retrieving full document context based on relevant knowledge IDs.

    This node analyzes the documents already retrieved by previous nodes,
    identifies the most relevant knowledge sources, and fetches complete
    document context for those sources.

    Runtime Requirements: State must have:
    - messages: List[BaseMessage] (for fallback query)
    - tasks: UserTasks (with docs already attached from previous retrieval)
    """

    NODE_NAME = "retrieve_full_documents_context"
    CONFIG_TYPES = (RetrieverConfig,)

    def __init__(
        self,
        vector_store,
        config_extractor: Optional[ConfigExtractor] = None,
        node_name: Optional[str] = None,
    ):
        super().__init__(config_extractor, node_name)
        self.vector_store = vector_store

    def validate_input_state(self, state) -> None:
        """Validate that state has the required attributes."""

        if "messages" not in state:
            raise NodeValidationError(
                "RetrieveFullDocumentsNode requires 'messages' attribute in state"
            )

        if not state["messages"]:
            raise NodeValidationError(
                "RetrieveFullDocumentsNode requires non-empty messages in state"
            )

        # Check that vector store has the required method
        if not hasattr(self.vector_store, "get_vectors_by_knowledge_id"):
            raise NodeValidationError(
                "Vector store must have method 'get_vectors_by_knowledge_id', "
                "this is an enterprise only feature"
            )

    def validate_output_state(self, state) -> None:
        """Validate that output state has tasks with updated documents."""
        pass

    def _analyze_relevant_knowledge(
        self, docs, retriever_config: RetrieverConfig
    ) -> OrderedDict:
        """
        Analyze documents to identify the most relevant knowledge sources.

        Args:
            docs: List of documents with metadata

        Returns:
            OrderedDict of top knowledge IDs with their relevance info
        """
        relevant_knowledge: Dict[str, Dict[str, Any]] = {}

        for doc in docs:
            knowledge_id = doc.metadata["knowledge_id"]
            similarity_score = doc.metadata.get("similarity", 0)

            if knowledge_id in relevant_knowledge:
                relevant_knowledge[knowledge_id]["count"] += 1
                relevant_knowledge[knowledge_id]["max_similarity_score"] = max(
                    relevant_knowledge[knowledge_id]["max_similarity_score"],
                    similarity_score,
                )
                relevant_knowledge[knowledge_id]["chunk_index"] = max(
                    doc.metadata["chunk_index"],
                    relevant_knowledge[knowledge_id]["chunk_index"],
                )
            else:
                relevant_knowledge[knowledge_id] = {
                    "count": 1,
                    "max_similarity_score": similarity_score,
                    "chunk_index": doc.metadata["chunk_index"],
                }

        # Sort by relevance and take top N
        top_n = min(retriever_config.top_n_knowledge, len(relevant_knowledge))
        top_knowledge_ids = OrderedDict(
            sorted(
                relevant_knowledge.items(),
                key=lambda x: (
                    x[1]["max_similarity_score"],
                    x[1]["count"],
                ),
                reverse=True,
            )[:top_n]
        )

        self.logger.info(f"Top knowledge IDs: {top_knowledge_ids}")
        return top_knowledge_ids

    async def execute(self, state, config: Optional[BaseGraphConfig] = None):
        """Execute full document context retrieval."""

        # Get config using the injected extractor
        retriever_config, _ = self.get_config(RetrieverConfig, config)

        # Get or create tasks
        if "tasks" in state and state["tasks"]:
            tasks = state["tasks"]
        else:
            # Fallback: create tasks from first message
            tasks = UserTasks([state["messages"][0].content])

        if not tasks.has_tasks():
            return {**state}

        # Get existing documents from tasks
        docs = tasks.docs if tasks else []

        if not docs:
            self.logger.warning(
                "No documents found in tasks for full context retrieval"
            )
            return {**state}

        # Analyze documents to find most relevant knowledge sources
        top_knowledge_ids = self._analyze_relevant_knowledge(docs, retriever_config)

        if not top_knowledge_ids:
            self.logger.warning("No relevant knowledge IDs found")
            return {**state}

        # Retrieve full documents for top knowledge sources
        full_docs = []
        for knowledge_id, knowledge_info in top_knowledge_ids.items():
            try:
                docs_for_knowledge = (
                    await self.vector_store.get_vectors_by_knowledge_id(
                        knowledge_id,
                        end_index=knowledge_info["chunk_index"],
                    )
                )
                full_docs.extend(docs_for_knowledge)

                self.logger.debug(
                    f"Retrieved {len(docs_for_knowledge)} documents for knowledge_id: {knowledge_id}"
                )

            except Exception as e:
                self.logger.error(
                    f"Failed to retrieve full documents for knowledge_id {knowledge_id}: {str(e)}"
                )

        # Update tasks with full documents
        # Note: This currently only handles the first task (as per original FIXME comment)
        if tasks.ids and full_docs:
            tasks.set_docs(tasks.ids[0], full_docs)
            self.logger.info(
                f"Set {len(full_docs)} full documents for task {tasks.ids[0]}"
            )

        return {**state, "tasks": tasks}
