from uuid import UUID
from typing import AsyncGenerator, Any, Type


from quivr_core.base_config import QuivrBaseConfig
from quivr_core.rag.entities.chat import ChatHistory
from quivr_core.rag.entities.models import ParsedRAGChunkResponse, QuivrKnowledge
from langchain.schema.messages import AIMessageChunk
from langchain_core.runnables.schema import StreamEvent
from langchain_core.documents import Document

from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.entities.models import (
    RAGResponseMetadata,
)
from quivr_core.rag.entities.config import (
    WorkflowConfig,
    NodeConfig,
)

import quivr_core.rag.langgraph_framework.nodes as _  # noqa: F401

from langgraph.graph import END, START
from quivr_core.rag.langgraph_framework.graph_builder import GraphBuilder
from quivr_core.rag.langgraph_framework.registry.node_registry import node_registry
from quivr_core.rag.langgraph_framework.services.service_container import (
    ServiceContainer,
)
from quivr_core.rag.utils import (
    LangfuseService,
    format_file_list,
    get_chunk_metadata,
    parse_chunk_response,
)
from quivr_core.rag.langgraph_framework.base.extractors import ConfigMapping

import logging

logger = logging.getLogger("quivr_core")

langfuse_service = LangfuseService()
langfuse_handler = langfuse_service.get_handler()


class QuivrQARAGLangGraphRefactored:
    def __init__(
        self,
        workflow_config: WorkflowConfig,
        graph_state,
        graph_config: dict[str, Any],
        graph_config_schema: Type[QuivrBaseConfig],
        llm_service: LLMService,
        config_extractor: ConfigMapping,
        service_container: ServiceContainer,
    ):
        self.workflow_config = workflow_config
        self.graph_state = graph_state
        self.graph_config = graph_config
        self.graph_config_schema = graph_config_schema
        self.llm_service = llm_service
        self.config_extractor = config_extractor
        self.service_container = service_container
        self.graph = None
        self.final_nodes: list[str] = []

        # Initialize GraphBuilder with custom state and config
        self.graph_builder = GraphBuilder(registry=node_registry)
        # Override the default graph with our custom state and config schema
        self.graph_builder.graph = self._create_custom_state_graph()

    def _create_custom_state_graph(self):
        """Create StateGraph with custom state and config schema."""
        from langgraph.graph import StateGraph

        return StateGraph(self.graph_state, config_schema=self.graph_config_schema)

    def _build_workflow_with_builder(self):
        """Build workflow using GraphBuilder with registered nodes."""
        # No need for auto-discovery - nodes are imported via __init__.py
        # Just log what's available
        available_nodes = node_registry.list_nodes()
        logger.info(f"Available nodes: {available_nodes}")

        if not available_nodes:
            raise RuntimeError(
                "No nodes found in registry. Make sure to import "
                "quivr_core.rag.langgraph_framework.nodes before using this class."
            )

        # Add all nodes from the workflow config using the registry
        for node in self.workflow_config.nodes:
            if node.name not in [START, END]:
                # Create node instance using the registry by node name
                try:
                    node_instance = node_registry.create_node(
                        node.name,
                        config_extractor=self.config_extractor,
                        service_container=self.service_container,
                    )
                    self.graph_builder.graph.add_node(node.name, node_instance)
                    self.graph_builder.nodes[node.name] = node_instance
                    logger.info(f"Added node '{node.name}' from registry")
                except KeyError:
                    available_nodes = node_registry.list_nodes()
                    raise ValueError(
                        f"Node '{node.name}' not found in registry. Available nodes: {available_nodes}"
                    )

        # Add edges using the workflow config
        for node in self.workflow_config.nodes:
            self._add_node_edges_with_builder(node)

        return self.graph_builder.graph

    def _add_node_edges_with_builder(self, node: NodeConfig):
        """Add node edges using the graph builder's graph."""
        if node.edges:
            for edge in node.edges:
                self.graph_builder.graph.add_edge(node.name, edge)
                if edge == END:
                    self.final_nodes.append(node.name)
        elif node.conditional_edge:
            routing_function = getattr(self, node.conditional_edge.routing_function)
            self.graph_builder.graph.add_conditional_edges(
                node.name, routing_function, node.conditional_edge.conditions
            )
            # Check if END is in conditions (handles both dict and list formats)
            conditions = node.conditional_edge.conditions
            if isinstance(conditions, dict):
                if END in conditions.values():
                    self.final_nodes.append(node.name)
            elif isinstance(conditions, list):
                if END in conditions:
                    self.final_nodes.append(node.name)
        else:
            raise ValueError("Node should have at least one edge or conditional_edge")

    def create_graph(self):
        """Create and compile the graph using GraphBuilder."""
        workflow = self._build_workflow_with_builder()
        # Reset final_nodes as they're populated during edge creation
        # (Note: final_nodes are populated in _add_node_edges_with_builder)

        return workflow.compile()

    def build_chain(self):
        """
        Builds the langchain chain for the given configuration.

        Returns:
            Callable[[Dict], Dict]: The langchain chain.
        """
        if not self.graph:
            self.graph = self.create_graph()

        return self.graph

    async def answer_astream(
        self,
        run_id: UUID,
        question: str,
        system_prompt: str | None,
        history: ChatHistory,
        list_files: list[QuivrKnowledge],
        metadata: dict[str, str] = {},
        **input_kwargs,
    ) -> AsyncGenerator[ParsedRAGChunkResponse, ParsedRAGChunkResponse]:
        """
        Answer a question using the langgraph chain and yield each chunk of the answer separately.
        """
        concat_list_files = format_file_list(list_files)
        conversational_qa_chain = self.build_chain()

        rolling_message = AIMessageChunk(content="")
        docs: list[Document] | None = None
        previous_content = ""
        system_prompt = system_prompt
        messages = [("system", system_prompt)] if system_prompt else []
        messages.append(("user", question))
        import os

        logger.info("OPENAI_API_KEY: %s", os.getenv("OPENAI_API_KEY"))

        async for event in conversational_qa_chain.astream_events(
            {
                "messages": messages,
                "chat_history": history,
                "files": concat_list_files,
                **input_kwargs,
            },
            version="v1",
            config={
                "configurable": self.graph_config,
                "run_id": run_id,
                "metadata": metadata,
                "callbacks": [langfuse_handler],
            },
        ):
            node_name = self._extract_node_name(event)

            if self._is_final_node_with_docs(event):
                event_data = event.get("data", {})
                if "output" in event_data and event_data["output"]:
                    tasks = event_data["output"].get("tasks")
                    docs = tasks.docs if tasks else []

            if self._is_final_node_and_chat_model_stream(event):
                event_data = event.get("data", {})
                if "chunk" in event_data:
                    chunk = event_data["chunk"]
                    rolling_message, new_content, previous_content = (
                        parse_chunk_response(
                            rolling_message,
                            chunk,
                            self.llm_service.supports_function_calling(),
                            previous_content,
                        )
                    )

                    if new_content:
                        chunk_metadata = get_chunk_metadata(rolling_message, docs)
                        if node_name:
                            chunk_metadata.workflow_step = node_name
                        yield ParsedRAGChunkResponse(
                            answer=new_content, metadata=chunk_metadata
                        )
            else:
                if node_name:
                    yield ParsedRAGChunkResponse(
                        answer="",
                        metadata=RAGResponseMetadata(workflow_step=node_name),
                    )

        # Yield final metadata chunk
        yield ParsedRAGChunkResponse(
            answer="",
            metadata=get_chunk_metadata(rolling_message, docs),
            last_chunk=True,
        )

    def _is_final_node_with_docs(self, event: StreamEvent) -> bool:
        event_data = event.get("data", {})
        event_metadata = event.get("metadata", {})
        return (
            "output" in event_data
            and event_data["output"] is not None
            and "tasks" in event_data["output"]
            and event_metadata.get("langgraph_node") in self.final_nodes
        )

    def _is_final_node_and_chat_model_stream(self, event: StreamEvent) -> bool:
        event_metadata = event.get("metadata", {})
        return (
            event.get("event") == "on_chat_model_stream"
            and "langgraph_node" in event_metadata
            and event_metadata.get("langgraph_node") in self.final_nodes
        )

    def _extract_node_name(self, event: StreamEvent) -> str:
        metadata = event.get("metadata", {})
        if "langgraph_node" in metadata:
            name = metadata["langgraph_node"]
            for node in self.workflow_config.nodes:
                if node.name == name:
                    if node.description:
                        return node.description
                    else:
                        return node.name
        return ""
