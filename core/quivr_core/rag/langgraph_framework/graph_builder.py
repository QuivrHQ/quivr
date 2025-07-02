from typing import Dict, Any, List, Optional
from langgraph.graph import StateGraph
import logging

from quivr_core.rag.langgraph_framework.registry.node_registry import (
    node_registry,
    NodeRegistry,
)
from quivr_core.rag.langgraph_framework.base.node import BaseNode
from quivr_core.rag.langgraph_framework.state import AgentState

logger = logging.getLogger("quivr_core")


class GraphBuilder:
    """Builder for creating LangGraph workflows using registered nodes."""

    def __init__(self, registry: Optional[NodeRegistry] = None):
        self.registry = registry or node_registry
        self.graph = StateGraph(AgentState)
        self.nodes: Dict[str, BaseNode] = {}

    def add_node(self, node_name: str, node_type: str, **node_kwargs) -> "GraphBuilder":
        """Add a node to the graph by type name."""
        try:
            node_instance = self.registry.create_node(node_type, **node_kwargs)
            self.graph.add_node(node_name, node_instance)
            self.nodes[node_name] = node_instance
            logger.info(f"Added node '{node_name}' of type '{node_type}'")
        except KeyError:
            available_nodes = self.registry.list_nodes()
            raise ValueError(
                f"Node type '{node_type}' not found. Available nodes: {available_nodes}"
            )
        return self

    def add_edge(self, from_node: str, to_node: str) -> "GraphBuilder":
        """Add an edge between nodes."""
        self.graph.add_edge(from_node, to_node)
        return self

    def add_conditional_edge(
        self, from_node: str, condition_func: Any, condition_map: dict[Any, str]
    ) -> "GraphBuilder":
        """Add a conditional edge."""
        self.graph.add_conditional_edges(from_node, condition_func, condition_map)
        return self

    def set_entry_point(self, node_name: str) -> "GraphBuilder":
        """Set the entry point of the graph."""
        self.graph.set_entry_point(node_name)
        return self

    def set_finish_point(self, node_name: str) -> "GraphBuilder":
        """Set the finish point of the graph."""
        self.graph.set_finish_point(node_name)
        return self

    def build(self):
        """Build and return the compiled graph."""
        return self.graph.compile()

    def list_available_nodes(self) -> Dict[str, List[str]]:
        """List all available node types by category."""
        result = {}
        for category in self.registry.list_categories():
            result[category] = self.registry.list_nodes(category)
        return result


# Example usage function
def create_rag_workflow() -> Any:
    """Example of creating a RAG workflow using the registry."""
    # Import nodes to ensure they're registered

    builder = GraphBuilder()

    # Build the workflow - nodes are already registered
    workflow = (
        builder.add_node("retrieve", "retrieve")
        .add_node("generate", "generate_rag")
        .add_edge("retrieve", "generate")
        .set_entry_point("retrieve")
        .set_finish_point("generate")
        .build()
    )

    return workflow
