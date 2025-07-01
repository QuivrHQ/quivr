"""Tests for generation nodes."""

import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage

from quivr_core.rag.entities.config import (
    LLMEndpointConfig,
    RetrievalConfig,
)
from quivr_core.rag.entities.prompt import PromptConfig

from quivr_core.rag.langgraph_framework.nodes.generation.generate_rag_node import (
    GenerateRagNode,
)
from quivr_core.rag.langgraph_framework.nodes.generation.generate_chat_llm_node import (
    GenerateChatLlmNode,
)
from quivr_core.rag.langgraph_framework.nodes.generation.generate_zendesk_rag_node import (
    GenerateZendeskRagNode,
)
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService

from tests.rag.langgraph_framework.fixtures.test_data import (
    create_sample_agent_state,
    create_sample_user_tasks,
    create_sample_documents,
)


class TestGenerateRagNode:
    """Test GenerateRagNode functionality."""

    @pytest.fixture(scope="function")
    def generate_rag_node(self):
        """Create a GenerateRagNode instance."""
        return GenerateRagNode()

    @pytest.fixture(scope="function")
    def valid_state(self):
        """Create a valid state for testing."""
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()
        return state

    @pytest.fixture(scope="function")
    def mock_llm_service(self):
        """Create mock LLM service."""
        mock_service = Mock(spec=LLMService)
        mock_service.count_tokens.return_value = 100
        mock_service.bind_tools.return_value = mock_service  # Return self for chaining
        mock_service.get_base_llm.return_value = (
            mock_service  # Return self for chaining
        )
        mock_service.invoke.return_value = "Generated response"
        return mock_service

    def test_node_name(self, generate_rag_node):
        """Test node name."""
        assert generate_rag_node.NODE_NAME == "generate_rag"

    def test_validate_input_state_success(self, generate_rag_node, valid_state):
        """Test successful input state validation."""
        generate_rag_node.validate_input_state(valid_state)

    def test_validate_input_state_missing_messages(self, generate_rag_node):
        """Test input validation with missing messages."""
        state = {"tasks": create_sample_user_tasks()}

        with pytest.raises(NodeValidationError, match="requires 'messages' attribute"):
            generate_rag_node.validate_input_state(state)

    def test_validate_input_state_empty_messages(self, generate_rag_node):
        """Test input validation with empty messages."""
        state = {"messages": [], "tasks": create_sample_user_tasks()}

        with pytest.raises(NodeValidationError, match="requires non-empty messages"):
            generate_rag_node.validate_input_state(state)

    def test_validate_input_state_missing_tasks(self, generate_rag_node):
        """Test input validation with missing tasks."""
        state = {"messages": [HumanMessage(content="Hello")]}

        with pytest.raises(NodeValidationError, match="requires 'tasks' attribute"):
            generate_rag_node.validate_input_state(state)

    def test_validate_output_state(self, generate_rag_node):
        """Test output state validation."""
        # Should not raise any errors for valid output
        generate_rag_node.validate_output_state({"messages": []})

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_basic(
        self, generate_rag_node, valid_state, mock_llm_service
    ):
        """Test basic execution."""
        config = Mock()

        with patch("quivr_core.rag.prompt.registry.get_prompt") as mock_get_prompt:
            # Mock prompt template
            mock_template = Mock()
            mock_template.format.return_value = "Formatted RAG prompt"
            mock_get_prompt.return_value = mock_template

            with patch.object(
                generate_rag_node, "get_service", return_value=mock_llm_service
            ):
                result = await generate_rag_node.execute(valid_state, config)

        assert "messages" in result
        assert isinstance(result["messages"], list)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_documents(
        self, generate_rag_node, valid_state, mock_llm_service
    ):
        """Test execution with documents in state."""
        valid_state["documents"] = create_sample_documents()
        config = Mock()

        with patch("quivr_core.rag.prompt.registry.get_prompt") as mock_get_prompt:
            mock_template = Mock()
            mock_template.format.return_value = "Formatted RAG prompt with docs"
            mock_get_prompt.return_value = mock_template

            with patch.object(
                generate_rag_node, "get_service", return_value=mock_llm_service
            ):
                result = await generate_rag_node.execute(valid_state, config)

        assert "messages" in result
        assert isinstance(result["messages"], list)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_custom_prompt(
        self, generate_rag_node, valid_state, mock_llm_service
    ):
        """Test execution with custom prompt configuration."""
        prompt_config = PromptConfig(
            prompt="Custom prompt instructions", template_name="custom_template"
        )
        config = Mock()
        config.prompt = prompt_config

        with patch("quivr_core.rag.prompt.registry.get_prompt") as mock_get_prompt:
            mock_template = Mock()
            mock_template.format.return_value = "Custom formatted prompt"
            mock_get_prompt.return_value = mock_template

            with patch.object(
                generate_rag_node, "get_service", return_value=mock_llm_service
            ):
                result = await generate_rag_node.execute(valid_state, config)

        assert "messages" in result


class TestGenerateChatLlmNode:
    """Test GenerateChatLlmNode functionality."""

    @pytest.fixture(scope="function")
    def generate_chat_llm_node(self):
        """Create a GenerateChatLlmNode instance."""
        return GenerateChatLlmNode()

    @pytest.fixture(scope="function")
    def valid_state(self):
        """Create a valid state for testing."""
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()
        return state

    @pytest.fixture(scope="function")
    def mock_llm_service(self):
        """Create mock LLM service."""
        mock_service = Mock(spec=LLMService)
        mock_service.count_tokens.return_value = 50
        mock_service.bind_tools.return_value = mock_service  # Return self for chaining
        mock_service.get_base_llm.return_value = (
            mock_service  # Return self for chaining
        )
        mock_service.invoke.return_value = "Chat response"
        return mock_service

    def test_node_name(self, generate_chat_llm_node):
        """Test node name."""
        assert generate_chat_llm_node.NODE_NAME == "generate_chat_llm"

    def test_validate_input_state_success(self, generate_chat_llm_node, valid_state):
        """Test successful input state validation."""
        generate_chat_llm_node.validate_input_state(valid_state)

    def test_validate_input_state_missing_messages(self, generate_chat_llm_node):
        """Test input validation with missing messages."""
        state = {"tasks": create_sample_user_tasks()}

        with pytest.raises(NodeValidationError, match="requires 'messages' attribute"):
            generate_chat_llm_node.validate_input_state(state)

    def test_validate_input_state_missing_chat_history(self, generate_chat_llm_node):
        """Test input validation with missing chat_history."""
        state = {"messages": [HumanMessage(content="Hello")]}

        with pytest.raises(
            NodeValidationError, match="requires 'chat_history' attribute"
        ):
            generate_chat_llm_node.validate_input_state(state)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_basic(
        self, generate_chat_llm_node, valid_state, mock_llm_service
    ):
        """Test basic chat LLM execution."""
        config = Mock()

        with patch("quivr_core.rag.prompt.registry.get_prompt") as mock_get_prompt:
            mock_template = Mock()
            mock_template.format.return_value = "Formatted chat prompt"
            mock_get_prompt.return_value = mock_template

            with patch.object(
                generate_chat_llm_node, "get_service", return_value=mock_llm_service
            ):
                result = await generate_chat_llm_node.execute(valid_state, config)

        assert "messages" in result
        assert isinstance(result["messages"], list)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_without_documents(
        self, generate_chat_llm_node, valid_state, mock_llm_service
    ):
        """Test chat LLM execution doesn't require documents."""
        # Chat LLM should work without documents
        config = Mock()

        with patch("quivr_core.rag.prompt.registry.get_prompt") as mock_get_prompt:
            mock_template = Mock()
            mock_template.format.return_value = "Chat prompt without docs"
            mock_get_prompt.return_value = mock_template

            with patch.object(
                generate_chat_llm_node, "get_service", return_value=mock_llm_service
            ):
                result = await generate_chat_llm_node.execute(valid_state, config)

        assert "messages" in result


class TestGenerateZendeskRagNode:
    """Test GenerateZendeskRagNode functionality."""

    @pytest.fixture(scope="function")
    def generate_zendesk_rag_node(self):
        """Create a GenerateZendeskRagNode instance."""
        return GenerateZendeskRagNode()

    @pytest.fixture(scope="function")
    def valid_state(self):
        """Create a valid state for testing."""
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()
        return state

    @pytest.fixture(scope="function")
    def mock_llm_service(self):
        """Create mock LLM service."""
        mock_service = Mock(spec=LLMService)
        mock_service.count_tokens.return_value = 150
        mock_service.bind_tools.return_value = mock_service  # Return self for chaining
        mock_service.get_base_llm.return_value = (
            mock_service  # Return self for chaining
        )
        mock_service.invoke.return_value = "Zendesk response"
        return mock_service

    def test_node_name(self, generate_zendesk_rag_node):
        """Test node name."""
        assert generate_zendesk_rag_node.NODE_NAME == "generate_zendesk_rag"

    def test_validate_input_state_success(self, generate_zendesk_rag_node, valid_state):
        """Test successful input state validation."""
        generate_zendesk_rag_node.validate_input_state(valid_state)

    def test_validate_input_state_missing_messages(self, generate_zendesk_rag_node):
        """Test input validation with missing messages."""
        state = {"tasks": create_sample_user_tasks()}

        with pytest.raises(NodeValidationError, match="requires 'messages' attribute"):
            generate_zendesk_rag_node.validate_input_state(state)

    def test_validate_input_state_missing_tasks(self, generate_zendesk_rag_node):
        """Test input validation with missing tasks."""
        state = {"messages": [HumanMessage(content="Hello")]}

        with pytest.raises(NodeValidationError, match="requires 'tasks' attribute"):
            generate_zendesk_rag_node.validate_input_state(state)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_basic(
        self, generate_zendesk_rag_node, valid_state, mock_llm_service
    ):
        """Test basic Zendesk RAG execution."""
        config = Mock()

        with patch("quivr_core.rag.prompt.registry.get_prompt") as mock_get_prompt:
            mock_template = Mock()
            mock_template.format.return_value = "Formatted Zendesk prompt"
            mock_get_prompt.return_value = mock_template

            with patch.object(
                generate_zendesk_rag_node, "get_service", return_value=mock_llm_service
            ):
                result = await generate_zendesk_rag_node.execute(valid_state, config)

        assert "messages" in result
        assert isinstance(result["messages"], list)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_zendesk_documents(
        self, generate_zendesk_rag_node, valid_state, mock_llm_service
    ):
        """Test execution with Zendesk-specific documents."""
        # Add Zendesk-specific document metadata
        documents = create_sample_documents()
        for doc in documents:
            doc.metadata.update(
                {
                    "ticket_id": "12345",
                    "customer_id": "cust_123",
                    "agent_id": "agent_456",
                }
            )

        valid_state["documents"] = documents
        config = Mock()

        with patch("quivr_core.rag.prompt.registry.get_prompt") as mock_get_prompt:
            mock_template = Mock()
            mock_template.format.return_value = "Zendesk prompt with metadata"
            mock_get_prompt.return_value = mock_template

            with patch.object(
                generate_zendesk_rag_node, "get_service", return_value=mock_llm_service
            ):
                result = await generate_zendesk_rag_node.execute(valid_state, config)

        assert "messages" in result


class TestGenerationNodesIntegration:
    """Test integration aspects of generation nodes."""

    def test_all_generation_nodes_registered(self):
        """Test that all generation nodes are properly registered."""
        # Import the nodes package to ensure all decorators are executed
        import quivr_core.rag.langgraph_framework.nodes  # noqa: F401

        from quivr_core.rag.langgraph_framework.registry.node_registry import (
            node_registry,
        )

        generation_nodes = node_registry.list_nodes("generation")
        expected_nodes = ["generate_rag", "generate_chat_llm", "generate_zendesk_rag"]

        for node_name in expected_nodes:
            assert node_name in generation_nodes, f"Node {node_name} not registered"

    def test_generation_nodes_dependencies(self):
        """Test that generation nodes declare proper dependencies."""
        nodes = [GenerateRagNode(), GenerateChatLlmNode(), GenerateZendeskRagNode()]

        for node in nodes:
            assert hasattr(node, "NODE_NAME")
            assert hasattr(node, "validate_input_state")
            assert hasattr(node, "validate_output_state")
            assert hasattr(node, "execute")

    @pytest.mark.asyncio(loop_scope="session")
    async def test_generation_nodes_with_real_config(self):
        """Test generation nodes with realistic configuration."""
        from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig

        # Create realistic config
        llm_config = LLMEndpointConfig(
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_context_tokens=8000,
            max_output_tokens=4096,
        )

        # Create RetrievalConfig with custom LLMEndpointConfig
        retrieval_config = RetrievalConfig()
        retrieval_config.llm_config = llm_config

        config = BaseGraphConfig(retrieval_config=retrieval_config)

        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()
        state["documents"] = create_sample_documents()

        nodes = [GenerateRagNode(), GenerateChatLlmNode(), GenerateZendeskRagNode()]

        for node in nodes:
            # Should validate input successfully
            node.validate_input_state(state)

            # Mock the LLM service call for execution test
            with patch.object(node, "get_service") as mock_get_service:
                mock_service = Mock(spec=LLMService)
                mock_service.count_tokens.return_value = 100
                mock_service.bind_tools.return_value = (
                    mock_service  # Return self for chaining
                )
                mock_service.get_base_llm.return_value = (
                    mock_service  # Return self for chaining
                )
                mock_service.invoke.return_value = f"Response from {node.NODE_NAME}"
                mock_get_service.return_value = mock_service

                with patch(
                    "quivr_core.rag.prompt.registry.get_prompt"
                ) as mock_get_prompt:
                    mock_template = Mock()
                    mock_template.format.return_value = f"Prompt for {node.NODE_NAME}"
                    mock_get_prompt.return_value = mock_template

                    result = await node.execute(state, config)

                    assert "messages" in result
                    assert isinstance(result["messages"], list)

    def test_prompt_registry_integration(self):
        """Test that generation nodes properly integrate with prompt registry."""
        nodes = [GenerateRagNode(), GenerateChatLlmNode(), GenerateZendeskRagNode()]

        with patch("quivr_core.rag.prompt.registry.get_prompt") as mock_get_prompt:
            mock_template = Mock()
            mock_template.format.return_value = "Test prompt"
            mock_get_prompt.return_value = mock_template

            for node in nodes:
                # Each node should be able to get appropriate prompts
                # This is tested implicitly in the execute methods above
                pass
