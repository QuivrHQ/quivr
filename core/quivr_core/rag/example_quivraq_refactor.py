from quivr_core.rag.langgraph_framework.entities.filter_history_config import (
    FilterHistoryConfig,
)
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.services.service_container import (
    ServiceContainer,
)
from quivr_core.rag.langgraph_framework.registry.node_registry import node_registry
from quivr_core.rag.entities.config import (
    LLMEndpointConfig,
    WorkflowConfig,
    QuivrBaseConfig,
    RetrievalConfig,
)
from quivr_core.rag.entities.retriever import RetrieverConfig
from quivr_core.rag.entities.reranker import RerankerConfig
from typing import Dict, Any, Annotated, Sequence, List, Optional, TypedDict
from quivr_core.rag.entities.prompt import PromptConfig
from quivr_core.rag.quivr_rag_langgraph_refactored import QuivrQARAGLangGraphRefactored
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from quivr_core.rag.entities.chat import ChatHistory
from quivr_core.rag.langgraph_framework.task import UserTasks
from quivr_core.rag.entities.config import DefaultWorkflow
from quivr_core.rag.langgraph_framework.base.extractors import ConfigMapping

from dotenv import load_dotenv, find_dotenv
import logging
import sys
import uuid
import asyncio

# Add this import at the top to trigger node registration

load_dotenv(find_dotenv())

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class GeneralConfig(QuivrBaseConfig):
    llm_config: LLMEndpointConfig = LLMEndpointConfig()
    prompt_config: PromptConfig = PromptConfig()
    workflow_config: WorkflowConfig = WorkflowConfig()
    filter_history_config: FilterHistoryConfig = FilterHistoryConfig()


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    reasoning: List[str]
    chat_history: ChatHistory
    files: str
    tasks: UserTasks
    instructions: str
    ticket_metadata: Optional[dict[str, str]]
    user_metadata: Optional[dict[str, str]]
    additional_information: Optional[dict[str, str]]
    tool: str
    guidelines: str
    enforced_system_prompt: str
    _filter: Optional[Dict[str, Any]]
    ticket_history: str


async def main():
    logger.info("Starting Quivr RAG LangGraph Refactor with new architecture")

    # Create service container
    logger.info("Creating service container")
    service_container = ServiceContainer()

    # Create a single config extractor that knows how to extract all config types
    config_extractor = ConfigMapping(
        {
            PromptConfig: "prompt_config",
            LLMEndpointConfig: "llm_config",
            WorkflowConfig: "workflow_config",
            FilterHistoryConfig: "filter_history_config",
        }
    )

    # Nodes are already registered via import, just log what's available
    logger.info("Available nodes by category:")
    for category in node_registry.list_categories():
        nodes = node_registry.list_nodes(category)
        logger.info(f"  {category}: {nodes}")

    # Create workflow config
    logger.info("Creating workflow config")
    workflow_config = WorkflowConfig(nodes=DefaultWorkflow.CHAT_WITH_LLM.nodes)

    # Create graph configuration
    logger.info("Creating graph configuration")
    graph_schema = GeneralConfig
    graph_config = {"llm_config": {"model": "gpt-4o-mini"}}

    # Create QuivrQARAGLangGraphRefactored instance
    logger.info("Creating Quivr RAG LangGraph Refactor instance")

    # Get LLM service from container for backward compatibility
    llm_config = LLMEndpointConfig()
    llm_service = service_container.get_service(LLMService, llm_config)

    quivr_rag_langgraph = QuivrQARAGLangGraphRefactored(
        workflow_config=workflow_config,
        graph_state=AgentState,
        graph_config=graph_config,
        graph_config_schema=graph_schema,
        llm_service=llm_service,
        config_extractor=config_extractor,
        service_container=service_container,
    )
    logger.info("Quivr RAG LangGraph Refactor instance created successfully")

    # Test the system
    run_id = uuid.uuid4()
    question = "What is the capital of France?"
    chat_history = ChatHistory(chat_id=uuid.uuid4(), brain_id=uuid.uuid4())

    logger.info(f"Starting conversation with question: {question}")

    try:
        async for response in quivr_rag_langgraph.answer_astream(
            run_id,
            question,
            system_prompt=None,
            history=chat_history,
            list_files=[],
            metadata={},
        ):
            print(f"Response: {response}")
    except Exception as e:
        logger.error(f"Error during conversation: {e}", exc_info=True)


async def test_node_specific_config():
    """Test node-specific configuration with inheritance and overrides."""
    logger.info("Testing node-specific configuration behavior")

    # Create a config with global settings and node-specific overrides
    global_config = {
        "llm_config": {
            "model": "gpt-4o-mini",
            "temperature": 0.3,
            "max_context_tokens": 20000,
        },
        "filter_history_config": {"max_history": 10},
        # Node-specific overrides
        "nodes": {
            "filter_history": {
                "filter_history_config": {
                    "max_history": 5,  # Override global max_history
                }
            },
            "generate_rag": {
                "llm_config": {
                    "temperature": 0.1  # Different override for generate_rag node
                    # model and max_context_tokens will inherit from global
                }
            },
        },
    }

    config_extractor = ConfigMapping(
        {
            PromptConfig: "prompt_config",
            LLMEndpointConfig: "llm_config",
            WorkflowConfig: "workflow_config",
            FilterHistoryConfig: "filter_history_config",
        }
    )

    # Test global config extraction (no node name)
    logger.info("Testing global config extraction:")
    global_llm_config = config_extractor.extract(global_config, LLMEndpointConfig)
    logger.info(
        f"Global LLM config: model={global_llm_config.model}, temp={global_llm_config.temperature}"
    )

    global_filter_config = config_extractor.extract(global_config, FilterHistoryConfig)
    logger.info(f"Global Filter config: max_history={global_filter_config.max_history}")

    # Test node-specific config extraction with overrides
    logger.info("\nTesting node-specific config extraction:")

    # filter_history node - should have overridden values
    filter_node_llm_config = config_extractor.extract(
        global_config, LLMEndpointConfig, "filter_history"
    )
    logger.info(
        f"filter_history LLM config: model={filter_node_llm_config.model}, temp={filter_node_llm_config.temperature}, max_tokens={filter_node_llm_config.max_context_tokens}"
    )

    filter_node_filter_config = config_extractor.extract(
        global_config, FilterHistoryConfig, "filter_history"
    )
    logger.info(
        f"filter_history Filter config: max_history={filter_node_filter_config.max_history}"
    )

    # generate_rag node - should have partial overrides
    generate_node_llm_config = config_extractor.extract(
        global_config, LLMEndpointConfig, "generate_rag"
    )
    logger.info(
        f"generate_rag LLM config: model={generate_node_llm_config.model}, temp={generate_node_llm_config.temperature}, max_tokens={generate_node_llm_config.max_context_tokens}"
    )

    # non-existent node - should return global config
    unknown_node_llm_config = config_extractor.extract(
        global_config, LLMEndpointConfig, "unknown_node"
    )
    logger.info(
        f"unknown_node LLM config: model={unknown_node_llm_config.model}, temp={unknown_node_llm_config.temperature}"
    )

    # Verify the inheritance/override behavior
    assert global_llm_config.model == "gpt-4o-mini"
    assert global_llm_config.temperature == 0.3

    assert filter_node_llm_config.model == "gpt-4o-mini"  # Inherited (corrected)
    assert filter_node_llm_config.temperature == 0.3  # Inherited (corrected)
    assert filter_node_llm_config.max_context_tokens == 20000  # Inherited

    assert generate_node_llm_config.model == "gpt-4o-mini"  # Inherited
    assert generate_node_llm_config.temperature == 0.1  # Overridden
    assert generate_node_llm_config.max_context_tokens == 20000  # Inherited

    assert filter_node_filter_config.max_history == 5  # Overridden

    logger.info("✅ Node-specific configuration test passed!")


async def test_workflow_with_node_configs():
    """Test workflow configuration with node-specific configs and validation."""
    logger.info("Testing workflow configuration with node-specific configs")

    # Your desired JSON structure with node-specific configs
    config_data = {
        "llm_config": {
            "temperature": 0.3,
            "max_context_tokens": 20000,
            "model": "gpt-4o-mini",
        },
        "reranker_config": {"model": "rerank-v3.5", "top_n": 10, "supplier": "cohere"},
        "workflow_config": {
            "name": "Standard RAG",
            "nodes": [
                {
                    "name": "START",
                    "edges": ["filter_history"],
                    "description": "Starting workflow",
                },
                {
                    "name": "filter_history",
                    "edges": ["retrieve"],
                    "filter_history_config": {"max_history": 5},
                    "description": "Filtering history",
                },
                {
                    "name": "retrieve",
                    "edges": ["generate_zendesk_rag"],
                    "retriever_config": {
                        "k": 15,
                    },
                    "description": "Retrieving relevant information",
                },
                {
                    "name": "generate_zendesk_rag",
                    "edges": ["END"],
                    "llm_config": {
                        "temperature": 0.1  # Different temperature for generation
                    },
                    "description": "Generating answer",
                },
            ],
        },
    }

    try:
        # Test creating RetrievalConfig from this structure
        logger.info("Creating RetrievalConfig from JSON structure...")
        retrieval_config = RetrievalConfig.model_validate(config_data)
        logger.info("✅ RetrievalConfig created successfully")

        # Inspect the workflow config
        workflow = retrieval_config.workflow_config
        logger.info(f"Workflow name: {workflow.name}")
        logger.info(f"Number of nodes: {len(workflow.nodes)}")

        # Check each node for configs
        for node in workflow.nodes:
            logger.info(f"\nNode: {node.name}")
            logger.info(f"  Description: {node.description}")
            logger.info(f"  Edges: {node.edges}")

            # Check for node-specific configs (these would be raw dicts currently)
            node_dict = node.model_dump()
            for key, value in node_dict.items():
                if key.endswith("_config") and key != "conditional_edge":
                    logger.info(f"  {key}: {value}")

        # Test config extraction with the new structure
        config_extractor = ConfigMapping(
            {
                FilterHistoryConfig: "filter_history_config",
                LLMEndpointConfig: "llm_config",
                RetrieverConfig: "retriever_config",
                RerankerConfig: "reranker_config",
            }
        )

        # Test extracting configs for specific nodes
        logger.info("\nTesting config extraction for nodes:")

        # Extract filter_history config
        filter_config = config_extractor.extract(
            config_data, FilterHistoryConfig, "filter_history"
        )
        logger.info(f"filter_history max_history: {filter_config.max_history}")

        # Extract retriever config for retrieve node
        retriever_config = config_extractor.extract(
            config_data, RetrieverConfig, "retrieve"
        )
        logger.info(f"retrieve node k: {retriever_config.k}")

        # Extract LLM config for generate node (should have overridden temperature)
        llm_config_generate = config_extractor.extract(
            config_data, LLMEndpointConfig, "generate_zendesk_rag"
        )
        logger.info(
            f"generate_zendesk_rag temperature: {llm_config_generate.temperature}"
        )
        logger.info(
            f"generate_zendesk_rag model: {llm_config_generate.model}"
        )  # Should inherit

        logger.info("✅ Workflow with node configs test passed!")

    except Exception as e:
        logger.error(f"❌ Error testing workflow config: {e}", exc_info=True)
        raise


async def test_config_validation_errors():
    """Test that invalid configs are properly caught."""
    logger.info("Testing config validation error handling")

    # Test with invalid filter_history_config
    invalid_config = {
        "workflow_config": {
            "name": "Test Workflow",
            "nodes": [
                {
                    "name": "filter_history",
                    "edges": ["END"],
                    "filter_history_config": {
                        "max_history": "invalid_string"  # Should be int
                    },
                }
            ],
        }
    }

    try:
        # This should fail validation if we implement proper validation
        _ = RetrievalConfig.model_validate(invalid_config)
        logger.warning("⚠️ Invalid config was accepted - validation not yet implemented")
    except Exception as e:
        logger.info(f"✅ Validation correctly caught error: {e}")


if __name__ == "__main__":
    # Run all tests
    # asyncio.run(test_node_specific_config())
    # asyncio.run(test_workflow_with_node_configs())
    # asyncio.run(test_config_validation_errors())
    asyncio.run(main())
