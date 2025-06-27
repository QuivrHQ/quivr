"""Tests for generation nodes."""

import pytest
from unittest.mock import Mock, patch
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from quivr_core.rag.entities.config import (
    LLMEndpointConfig,
    WorkflowConfig,
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
from quivr_core.rag.langgraph_framework.services.rag_prompt_service import (
    RAGPromptService,
)

from tests.rag.langgraph_framework.fixtures.test_data import (
    create_sample_agent_state,
    create_sample_user_tasks,
    create_sample_documents,
    create_sample_chat_history,
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
    def mock_services(self):
        """Create mock services."""
        mock_llm_service = Mock(spec=LLMService)
        mock_prompt_service = Mock(spec=RAGPromptService)

        # Mock LLM service methods
        mock_llm_service.count_tokens.return_value = 100
        mock_llm_service.bind_tools.return_value = Mock()

        # Mock prompt service
        mock_template = Mock()
        mock_template.format.return_value = "Formatted prompt"
        mock_prompt_service.get_template.return_value = mock_template

        return mock_llm_service, mock_prompt_service, mock_template

    def test_node_name(self, generate_rag_node):
        """Test node name and configuration types."""
        assert generate_rag_node.NODE_NAME == "generate_rag"

    def test_validate_input_state_success(self, generate_rag_node, valid_state):
        """Test successful input state validation."""
        # Should not raise any exception
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
        state = {"messages": [HumanMessage(content="test")]}

        with pytest.raises(NodeValidationError, match="requires 'tasks' attribute"):
            generate_rag_node.validate_input_state(state)

    def test_validate_input_state_empty_tasks(self, generate_rag_node):
        """Test input validation with empty tasks."""
        state = {"messages": [HumanMessage(content="test")], "tasks": None}

        with pytest.raises(NodeValidationError, match="requires non-empty tasks"):
            generate_rag_node.validate_input_state(state)

    def test_validate_input_state_missing_files(self, generate_rag_node):
        """Test input validation with missing files."""
        state = {
            "messages": [HumanMessage(content="test")],
            "tasks": create_sample_user_tasks(),
        }

        with pytest.raises(NodeValidationError, match="requires 'files' attribute"):
            generate_rag_node.validate_input_state(state)

    def test_validate_input_state_missing_chat_history(self, generate_rag_node):
        """Test input validation with missing chat_history."""
        state = {
            "messages": [HumanMessage(content="test")],
            "tasks": create_sample_user_tasks(),
            "files": [],
        }

        with pytest.raises(
            NodeValidationError, match="requires 'chat_history' attribute"
        ):
            generate_rag_node.validate_input_state(state)

    def test_validate_input_state_invalid_chat_history(self, generate_rag_node):
        """Test input validation with chat_history missing required methods."""
        state = {
            "messages": [HumanMessage(content="test")],
            "tasks": create_sample_user_tasks(),
            "files": [],
            "chat_history": "invalid_chat_history",  # String without to_list method
        }

        with pytest.raises(
            NodeValidationError,
            match="requires chat_history object with 'to_list' method",
        ):
            generate_rag_node.validate_input_state(state)

    def test_validate_output_state(self, generate_rag_node):
        """Test output state validation (currently no-op)."""
        # Should not raise any exception
        generate_rag_node.validate_output_state({})

    def test_build_rag_prompt_inputs_with_docs(self, generate_rag_node, valid_state):
        """Test building RAG prompt inputs with documents."""
        docs = create_sample_documents()
        prompt = "Custom prompt"

        with patch(
            "quivr_core.rag.langgraph_framework.nodes.generation.generate_rag_node.combine_documents"
        ) as mock_combine:
            mock_combine.return_value = "Combined document content"

            result = generate_rag_node._build_rag_prompt_inputs(
                valid_state, prompt, docs
            )

        assert result["context"] == "Combined document content"
        assert result["task"] == valid_state["messages"][0].content
        assert result["custom_instructions"] == prompt
        assert result["files"] == valid_state["files"]
        mock_combine.assert_called_once_with(docs)

    def test_build_rag_prompt_inputs_no_docs(self, generate_rag_node, valid_state):
        """Test building RAG prompt inputs without documents."""
        result = generate_rag_node._build_rag_prompt_inputs(valid_state, None, None)

        assert result["context"] == "None"
        assert result["custom_instructions"] == "None"

    def test_build_rag_prompt_inputs_with_chat_history(
        self, generate_rag_node, valid_state
    ):
        """Test building RAG prompt inputs with chat history."""
        chat_history = create_sample_chat_history()
        valid_state["chat_history"] = chat_history

        result = generate_rag_node._build_rag_prompt_inputs(valid_state, None, None)

        assert result["chat_history"] == chat_history.to_list()

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_success(self, generate_rag_node, valid_state, mock_services):
        """Test successful execution."""
        mock_llm_service, mock_prompt_service, mock_template = mock_services

        # Mock the LLM response
        mock_llm = Mock()
        mock_response = AIMessage(content="Generated response")
        mock_llm.invoke.return_value = mock_response
        mock_llm_service.bind_tools.return_value = mock_llm

        # Mock service injection
        with patch.object(generate_rag_node, "get_service") as mock_get_service:
            mock_get_service.side_effect = [mock_prompt_service, mock_llm_service]

            # Mock config extraction
            with patch.object(generate_rag_node, "get_config") as mock_get_config:
                mock_get_config.side_effect = [
                    WorkflowConfig(),
                    PromptConfig(),
                    RetrievalConfig(),
                    LLMEndpointConfig(),
                ]

                # Mock context reduction
                with patch(
                    "quivr_core.rag.langgraph_framework.nodes.generation.generate_rag_node.reduce_rag_context"
                ) as mock_reduce:
                    mock_reduce.return_value = (valid_state, {"test": "inputs"})

                    result = await generate_rag_node.execute(valid_state)

        assert "messages" in result
        assert result["messages"] == [mock_response]
        mock_llm.invoke.assert_called_once()

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_custom_config(
        self, generate_rag_node, valid_state, mock_services
    ):
        """Test execution with custom configuration."""
        mock_llm_service, mock_prompt_service, mock_template = mock_services

        custom_config = Mock()
        mock_llm = Mock()
        mock_response = AIMessage(content="Custom response")
        mock_llm.invoke.return_value = mock_response
        mock_llm_service.bind_tools.return_value = mock_llm

        with patch.object(generate_rag_node, "get_service") as mock_get_service:
            mock_get_service.side_effect = [mock_prompt_service, mock_llm_service]

            with patch.object(generate_rag_node, "get_config") as mock_get_config:
                mock_get_config.side_effect = [
                    WorkflowConfig(),
                    PromptConfig(),
                    RetrievalConfig(),
                    LLMEndpointConfig(),
                ]

                with patch(
                    "quivr_core.rag.langgraph_framework.nodes.generation.generate_rag_node.reduce_rag_context"
                ) as mock_reduce:
                    mock_reduce.return_value = (valid_state, {"test": "inputs"})

                    _ = await generate_rag_node.execute(valid_state, custom_config)

        # Should pass custom config to get_config calls
        for call in mock_get_config.call_args_list:
            assert call[0][1] == custom_config


class TestGenerateChatLlmNode:
    """Test GenerateChatLlmNode functionality."""

    @pytest.fixture(scope="function")
    def generate_chat_llm_node(self):
        """Create a GenerateChatLlmNode instance."""
        return GenerateChatLlmNode()

    @pytest.fixture(scope="function")
    def valid_chat_state(self):
        """Create a valid state for chat LLM testing."""
        return {
            "messages": [
                HumanMessage(content="Hello"),
                AIMessage(content="Hi there!"),
                HumanMessage(content="How are you?"),
            ],
            "chat_history": create_sample_chat_history(),
        }

    def test_node_name(self, generate_chat_llm_node):
        """Test node name and configuration types."""
        assert generate_chat_llm_node.NODE_NAME == "generate_chat_llm"

    def test_validate_input_state_success(
        self, generate_chat_llm_node, valid_chat_state
    ):
        """Test successful input state validation."""
        generate_chat_llm_node.validate_input_state(valid_chat_state)

    def test_validate_input_state_missing_messages(self, generate_chat_llm_node):
        """Test input validation with missing messages."""
        state = {}

        with pytest.raises(NodeValidationError, match="requires 'messages' attribute"):
            generate_chat_llm_node.validate_input_state(state)

    def test_validate_input_state_empty_messages(self, generate_chat_llm_node):
        """Test input validation with empty messages."""
        state = {"messages": []}

        with pytest.raises(NodeValidationError, match="requires non-empty messages"):
            generate_chat_llm_node.validate_input_state(state)

    def test_validate_input_state_missing_chat_history(self, generate_chat_llm_node):
        """Test input validation with missing chat_history."""
        state = {"messages": [HumanMessage(content="test")]}

        with pytest.raises(
            NodeValidationError, match="requires 'chat_history' attribute"
        ):
            generate_chat_llm_node.validate_input_state(state)

    def test_validate_input_state_invalid_chat_history(self, generate_chat_llm_node):
        """Test input validation with chat_history missing required methods."""
        state = {
            "messages": [HumanMessage(content="test")],
            "chat_history": "invalid_chat_history",  # String without to_list method
        }

        with pytest.raises(
            NodeValidationError,
            match="requires chat_history object with 'to_list' method",
        ):
            generate_chat_llm_node.validate_input_state(state)

    def test_validate_output_state(self, generate_chat_llm_node):
        """Test output state validation (currently no-op)."""
        generate_chat_llm_node.validate_output_state({})

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_success(self, generate_chat_llm_node, valid_chat_state):
        """Test successful execution."""
        mock_llm_service = Mock(spec=LLMService)
        mock_prompt_service = Mock(spec=RAGPromptService)
        mock_llm = Mock()
        mock_response = AIMessage(content="I'm doing well, thank you!")
        mock_llm.invoke.return_value = mock_response
        mock_llm_service.get_base_llm.return_value = mock_llm
        mock_llm_service.count_tokens.return_value = 100

        # Mock prompt template
        mock_template = Mock()
        mock_template.format.return_value = "Chat template"
        mock_prompt_service.get_template.return_value = mock_template

        with patch.object(generate_chat_llm_node, "get_service") as mock_get_service:
            mock_get_service.side_effect = [mock_llm_service, mock_prompt_service]

            with patch.object(generate_chat_llm_node, "get_config") as mock_get_config:
                mock_get_config.side_effect = [
                    PromptConfig(),
                    LLMEndpointConfig(),
                ]

                # Mock context reduction
                with patch(
                    "quivr_core.rag.langgraph_framework.nodes.generation.generate_chat_llm_node.reduce_rag_context"
                ) as mock_reduce:
                    mock_reduce.return_value = (valid_chat_state, {"test": "inputs"})

                    # Mock ChatPromptTemplate
                    with patch(
                        "quivr_core.rag.langgraph_framework.nodes.generation.generate_chat_llm_node.ChatPromptTemplate"
                    ) as mock_chat_template:
                        mock_prompt_instance = Mock()
                        mock_prompt_instance.invoke.return_value = "formatted_prompt"
                        mock_chat_template.from_messages.return_value = (
                            mock_prompt_instance
                        )

                        result = await generate_chat_llm_node.execute(valid_chat_state)

        assert "messages" in result
        assert result["messages"] == [mock_response]
        mock_llm.invoke.assert_called_once()

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_system_message(self, generate_chat_llm_node):
        """Test execution with system message in chat."""
        state_with_system = {
            "messages": [
                SystemMessage(content="You are a helpful assistant"),
                HumanMessage(content="Hello"),
            ],
            "chat_history": create_sample_chat_history(),
        }

        mock_llm_service = Mock(spec=LLMService)
        mock_prompt_service = Mock(spec=RAGPromptService)
        mock_llm = Mock()
        mock_response = AIMessage(content="Hello! How can I help you?")
        mock_llm.invoke.return_value = mock_response
        mock_llm_service.get_base_llm.return_value = mock_llm
        mock_llm_service.count_tokens.return_value = 50

        mock_template = Mock()
        mock_prompt_service.get_template.return_value = mock_template

        with patch.object(generate_chat_llm_node, "get_service") as mock_get_service:
            mock_get_service.side_effect = [mock_llm_service, mock_prompt_service]

            with patch.object(generate_chat_llm_node, "get_config") as mock_get_config:
                mock_get_config.side_effect = [
                    PromptConfig(),
                    LLMEndpointConfig(),
                ]

                with patch(
                    "quivr_core.rag.langgraph_framework.nodes.generation.generate_chat_llm_node.reduce_rag_context"
                ) as mock_reduce:
                    mock_reduce.return_value = (state_with_system, {"test": "inputs"})

                    with patch(
                        "quivr_core.rag.langgraph_framework.nodes.generation.generate_chat_llm_node.ChatPromptTemplate"
                    ) as mock_chat_template:
                        mock_prompt_instance = Mock()
                        mock_prompt_instance.invoke.return_value = "formatted_prompt"
                        mock_chat_template.from_messages.return_value = (
                            mock_prompt_instance
                        )

                        result = await generate_chat_llm_node.execute(state_with_system)

        assert result["messages"] == [mock_response]


class TestGenerateZendeskRagNode:
    """Test GenerateZendeskRagNode functionality."""

    @pytest.fixture(scope="function")
    def generate_zendesk_rag_node(self):
        """Create a GenerateZendeskRagNode instance."""
        return GenerateZendeskRagNode()

    @pytest.fixture(scope="function")
    def valid_zendesk_state(self):
        """Create a valid state for Zendesk RAG testing."""
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()
        state["ticket_metadata"] = {"ticket_id": "12345", "priority": "high"}
        state["user_metadata"] = {"user_id": "user123", "plan": "premium"}
        state["ticket_history"] = "Previous ticket interactions..."
        return state

    def test_node_name(self, generate_zendesk_rag_node):
        """Test node name and configuration types."""
        assert generate_zendesk_rag_node.NODE_NAME == "generate_zendesk_rag"

    def test_validate_input_state_success(
        self, generate_zendesk_rag_node, valid_zendesk_state
    ):
        """Test successful input state validation."""
        generate_zendesk_rag_node.validate_input_state(valid_zendesk_state)

    def test_validate_input_state_missing_messages(self, generate_zendesk_rag_node):
        """Test input validation with missing messages."""
        state = {"tasks": create_sample_user_tasks()}

        with pytest.raises(NodeValidationError, match="requires 'messages' attribute"):
            generate_zendesk_rag_node.validate_input_state(state)

    def test_validate_input_state_empty_messages(self, generate_zendesk_rag_node):
        """Test input validation with empty messages."""
        state = {"messages": [], "tasks": create_sample_user_tasks()}

        with pytest.raises(NodeValidationError, match="requires non-empty messages"):
            generate_zendesk_rag_node.validate_input_state(state)

    def test_validate_input_state_missing_tasks(self, generate_zendesk_rag_node):
        """Test input validation with missing tasks."""
        state = {"messages": [HumanMessage(content="test")]}

        with pytest.raises(NodeValidationError, match="requires 'tasks' attribute"):
            generate_zendesk_rag_node.validate_input_state(state)

    def test_validate_input_state_empty_tasks(self, generate_zendesk_rag_node):
        """Test input validation with empty tasks."""
        state = {"messages": [HumanMessage(content="test")], "tasks": None}

        with pytest.raises(NodeValidationError, match="requires non-empty tasks"):
            generate_zendesk_rag_node.validate_input_state(state)

    def test_validate_output_state(self, generate_zendesk_rag_node):
        """Test output state validation (currently no-op)."""
        generate_zendesk_rag_node.validate_output_state({})

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_success(
        self, generate_zendesk_rag_node, valid_zendesk_state
    ):
        """Test successful execution."""
        mock_llm_service = Mock(spec=LLMService)
        mock_prompt_service = Mock(spec=RAGPromptService)

        # Mock LLM and response
        mock_llm = Mock()
        mock_response = AIMessage(content="Zendesk response with ticket context")
        mock_llm.invoke.return_value = mock_response
        mock_llm_service.bind_tools.return_value = mock_llm

        # Mock prompt template
        mock_template = Mock()
        mock_template.input_variables = [
            "similar_tickets",
            "ticket_metadata",
            "user_metadata",
            "client_query",
            "ticket_history",
            "current_time",
        ]
        mock_template.format_prompt.return_value = "Formatted Zendesk prompt"
        mock_prompt_service.get_template.return_value = mock_template

        with patch.object(generate_zendesk_rag_node, "get_service") as mock_get_service:
            mock_get_service.side_effect = [mock_llm_service, mock_prompt_service]

            with patch.object(
                generate_zendesk_rag_node, "get_config"
            ) as mock_get_config:
                mock_get_config.side_effect = [
                    WorkflowConfig(),
                    LLMEndpointConfig(),
                ]

                # Mock datetime
                with patch(
                    "quivr_core.rag.langgraph_framework.nodes.generation.generate_zendesk_rag_node.datetime"
                ) as mock_datetime:
                    mock_datetime.now.return_value.strftime.return_value = (
                        "2024-01-01 12:00:00"
                    )

                    # Mock format_dict
                    with patch(
                        "quivr_core.rag.langgraph_framework.nodes.generation.generate_zendesk_rag_node.format_dict"
                    ) as mock_format_dict:
                        mock_format_dict.side_effect = lambda x: f"formatted_{x}"

                        result = await generate_zendesk_rag_node.execute(
                            valid_zendesk_state
                        )

        assert "messages" in result
        assert result["messages"] == [mock_response]
        mock_llm.invoke.assert_called_once()
        mock_template.format_prompt.assert_called_once()

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_missing_optional_metadata(
        self, generate_zendesk_rag_node
    ):
        """Test execution with missing optional metadata."""
        # State without ticket_metadata and user_metadata
        state = create_sample_agent_state()
        state["tasks"] = create_sample_user_tasks()
        state["ticket_metadata"] = None
        state["user_metadata"] = None

        mock_llm_service = Mock(spec=LLMService)
        mock_prompt_service = Mock(spec=RAGPromptService)

        mock_llm = Mock()
        mock_response = AIMessage(content="Response without metadata")
        mock_llm.invoke.return_value = mock_response
        mock_llm_service.bind_tools.return_value = mock_llm

        mock_template = Mock()
        mock_template.input_variables = [
            "similar_tickets",
            "ticket_metadata",
            "user_metadata",
            "client_query",
            "ticket_history",
            "current_time",
        ]
        mock_template.format_prompt.return_value = "Formatted prompt"
        mock_prompt_service.get_template.return_value = mock_template

        with patch.object(generate_zendesk_rag_node, "get_service") as mock_get_service:
            mock_get_service.side_effect = [mock_llm_service, mock_prompt_service]

            with patch.object(
                generate_zendesk_rag_node, "get_config"
            ) as mock_get_config:
                mock_get_config.side_effect = [
                    WorkflowConfig(),
                    LLMEndpointConfig(),
                ]

                with patch(
                    "quivr_core.rag.langgraph_framework.nodes.generation.generate_zendesk_rag_node.datetime"
                ) as mock_datetime:
                    mock_datetime.now.return_value.strftime.return_value = (
                        "2024-01-01 12:00:00"
                    )

                    with patch(
                        "quivr_core.rag.langgraph_framework.nodes.generation.generate_zendesk_rag_node.format_dict"
                    ) as mock_format_dict:
                        mock_format_dict.side_effect = lambda x: f"formatted_{x}"

                        result = await generate_zendesk_rag_node.execute(state)

        assert result["messages"] == [mock_response]

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_with_documents(
        self, generate_zendesk_rag_node, valid_zendesk_state
    ):
        """Test execution with documents in tasks."""
        # Add documents to tasks
        docs = create_sample_documents()
        valid_zendesk_state["tasks"].set_docs(valid_zendesk_state["tasks"].ids[0], docs)

        mock_llm_service = Mock(spec=LLMService)
        mock_prompt_service = Mock(spec=RAGPromptService)

        mock_llm = Mock()
        mock_response = AIMessage(content="Response with document context")
        mock_llm.invoke.return_value = mock_response
        mock_llm_service.bind_tools.return_value = mock_llm

        mock_template = Mock()
        mock_template.input_variables = [
            "similar_tickets",
            "ticket_metadata",
            "user_metadata",
            "client_query",
            "ticket_history",
            "current_time",
        ]
        mock_template.format_prompt.return_value = "Formatted prompt with docs"
        mock_prompt_service.get_template.return_value = mock_template

        with patch.object(generate_zendesk_rag_node, "get_service") as mock_get_service:
            mock_get_service.side_effect = [mock_llm_service, mock_prompt_service]

            with patch.object(
                generate_zendesk_rag_node, "get_config"
            ) as mock_get_config:
                mock_get_config.side_effect = [
                    WorkflowConfig(),
                    LLMEndpointConfig(),
                ]

                with patch(
                    "quivr_core.rag.langgraph_framework.nodes.generation.generate_zendesk_rag_node.datetime"
                ) as mock_datetime:
                    mock_datetime.now.return_value.strftime.return_value = (
                        "2024-01-01 12:00:00"
                    )

                    with patch(
                        "quivr_core.rag.langgraph_framework.nodes.generation.generate_zendesk_rag_node.format_dict"
                    ) as mock_format_dict:
                        mock_format_dict.side_effect = lambda x: f"formatted_{x}"

                        result = await generate_zendesk_rag_node.execute(
                            valid_zendesk_state
                        )

        # Verify that similar_tickets input contains document content
        call_args = mock_template.format_prompt.call_args[1]
        assert "similar_tickets" in call_args
        # Should contain content from the documents
        similar_tickets = call_args["similar_tickets"]
        assert any(doc.page_content in similar_tickets for doc in docs)

        assert result["messages"] == [mock_response]
