"""Tests for the Tool service."""

import pytest
from unittest.mock import Mock, AsyncMock, patch

from quivr_core.rag.entities.config import WorkflowConfig
from quivr_core.rag.langgraph_framework.services.tool_service import ToolService
from quivr_core.llm_tools.llm_tools import LLMToolFactory


class TestToolServiceInitialization:
    """Test Tool service initialization."""

    def test_initialization_with_config(self):
        """Test tool service initialization with workflow config."""
        workflow_config = WorkflowConfig()
        service = ToolService(workflow_config)

        assert service.workflow_config == workflow_config


class TestToolServiceNodeTools:
    """Test node-specific tool management."""

    @pytest.fixture(scope="function")
    def mock_tool_service(self):
        """Create a mock tool service."""
        workflow_config = Mock(spec=WorkflowConfig)
        service = ToolService(workflow_config)
        return service, workflow_config

    def test_get_node_tools(self, mock_tool_service):
        """Test getting tools for a specific node."""
        service, workflow_config = mock_tool_service
        workflow_config.get_node_tools.return_value = ["tool1", "tool2"]

        result = service.get_node_tools("test_node")

        assert result == ["tool1", "tool2"]
        workflow_config.get_node_tools.assert_called_once_with("test_node")


class TestToolServiceActivatedTools:
    """Test activated tools management."""

    @pytest.fixture(scope="function")
    def mock_tool_service_with_tools(self):
        """Create mock tool service with validated and activated tools."""
        workflow_config = Mock(spec=WorkflowConfig)

        # Mock tools
        mock_tool1 = Mock()
        mock_tool1.name = "tool1"
        mock_tool2 = Mock()
        mock_tool2.name = "tool2"
        mock_tool3 = Mock()
        mock_tool3.name = "tool3"

        workflow_config.validated_tools = [mock_tool1, mock_tool2, mock_tool3]
        workflow_config.activated_tools = [mock_tool1]  # Only tool1 is activated

        service = ToolService(workflow_config)
        return service, workflow_config, [mock_tool1, mock_tool2, mock_tool3]

    def test_get_activated_tools(self, mock_tool_service_with_tools):
        """Test getting activated tools."""
        service, workflow_config, tools = mock_tool_service_with_tools

        result = service.get_activated_tools()

        assert result == [tools[0]]  # Only tool1

    def test_get_validated_tools(self, mock_tool_service_with_tools):
        """Test getting validated tools."""
        service, workflow_config, tools = mock_tool_service_with_tools

        result = service.get_validated_tools()

        assert result == tools

    def test_activate_tools_single(self, mock_tool_service_with_tools):
        """Test activating a single tool."""
        service, workflow_config, tools = mock_tool_service_with_tools

        with patch(
            "quivr_core.rag.langgraph_framework.services.tool_service.logger"
        ) as mock_logger:
            service.activate_tools(["tool2"])

        assert tools[1] in workflow_config.activated_tools
        mock_logger.info.assert_called_with("Activated tool: tool2")

    def test_activate_tools_multiple(self, mock_tool_service_with_tools):
        """Test activating multiple tools."""
        service, workflow_config, tools = mock_tool_service_with_tools

        service.activate_tools(["tool2", "tool3"])

        assert tools[1] in workflow_config.activated_tools
        assert tools[2] in workflow_config.activated_tools

    def test_activate_tools_already_activated(self, mock_tool_service_with_tools):
        """Test activating already activated tool (should not duplicate)."""
        service, workflow_config, tools = mock_tool_service_with_tools
        initial_count = len(workflow_config.activated_tools)

        service.activate_tools(["tool1"])  # tool1 is already activated

        # Should not add duplicate
        assert len(workflow_config.activated_tools) == initial_count

    def test_activate_tools_nonexistent(self, mock_tool_service_with_tools):
        """Test activating non-existent tool (should be ignored)."""
        service, workflow_config, tools = mock_tool_service_with_tools
        initial_count = len(workflow_config.activated_tools)

        service.activate_tools(["nonexistent_tool"])

        assert len(workflow_config.activated_tools) == initial_count

    def test_deactivate_tools_single(self, mock_tool_service_with_tools):
        """Test deactivating a single tool."""
        service, workflow_config, tools = mock_tool_service_with_tools

        with patch(
            "quivr_core.rag.langgraph_framework.services.tool_service.logger"
        ) as mock_logger:
            service.deactivate_tools(["tool1"])

        assert tools[0] not in workflow_config.activated_tools
        mock_logger.info.assert_called_with("Deactivated tool: tool1")

    def test_deactivate_tools_multiple(self, mock_tool_service_with_tools):
        """Test deactivating multiple tools."""
        service, workflow_config, tools = mock_tool_service_with_tools

        # First activate tool2 and tool3
        workflow_config.activated_tools.extend([tools[1], tools[2]])

        service.deactivate_tools(["tool1", "tool2"])

        assert tools[0] not in workflow_config.activated_tools
        assert tools[1] not in workflow_config.activated_tools
        assert tools[2] in workflow_config.activated_tools  # Should remain

    def test_deactivate_tools_not_activated(self, mock_tool_service_with_tools):
        """Test deactivating non-activated tool (should be ignored)."""
        service, workflow_config, tools = mock_tool_service_with_tools
        initial_count = len(workflow_config.activated_tools)

        service.deactivate_tools(["tool2"])  # tool2 is not activated

        assert len(workflow_config.activated_tools) == initial_count

    def test_is_tool_activated_true(self, mock_tool_service_with_tools):
        """Test checking if tool is activated (true case)."""
        service, workflow_config, tools = mock_tool_service_with_tools

        assert service.is_tool_activated("tool1") is True

    def test_is_tool_activated_false(self, mock_tool_service_with_tools):
        """Test checking if tool is activated (false case)."""
        service, workflow_config, tools = mock_tool_service_with_tools

        assert service.is_tool_activated("tool2") is False


class TestToolServiceToolExecution:
    """Test tool creation and execution."""

    @pytest.fixture(scope="function")
    def mock_tool_service_for_execution(self):
        """Create mock tool service for execution testing."""
        workflow_config = Mock(spec=WorkflowConfig)

        # Mock activated tool
        mock_tool = Mock()
        mock_tool.name = "test_tool"
        workflow_config.activated_tools = [mock_tool]

        service = ToolService(workflow_config)
        return service, workflow_config

    def test_create_tool_instance_success(self, mock_tool_service_for_execution):
        """Test successful tool instance creation."""
        service, workflow_config = mock_tool_service_for_execution

        mock_tool_instance = Mock()

        with patch.object(
            LLMToolFactory, "create_tool", return_value=mock_tool_instance
        ) as mock_create:
            result = service.create_tool_instance("test_tool", {"param": "value"})

        assert result == mock_tool_instance
        mock_create.assert_called_once_with("test_tool", {"param": "value"})

    def test_create_tool_instance_default_config(self, mock_tool_service_for_execution):
        """Test tool instance creation with default config."""
        service, workflow_config = mock_tool_service_for_execution

        with patch.object(LLMToolFactory, "create_tool") as mock_create:
            service.create_tool_instance("test_tool")

        mock_create.assert_called_once_with("test_tool", {})

    def test_create_tool_instance_not_activated(self, mock_tool_service_for_execution):
        """Test tool instance creation for non-activated tool."""
        service, workflow_config = mock_tool_service_for_execution

        with pytest.raises(ValueError, match="Tool inactive_tool is not activated"):
            service.create_tool_instance("inactive_tool")

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_tool_success(self, mock_tool_service_for_execution):
        """Test successful tool execution."""
        service, workflow_config = mock_tool_service_for_execution

        # Mock tool wrapper
        mock_tool_wrapper = Mock()
        mock_tool_wrapper.format_input.return_value = "formatted_input"
        mock_tool_wrapper.format_output.return_value = "formatted_output"

        # Mock actual tool
        mock_tool = AsyncMock()
        mock_tool.ainvoke.return_value = "raw_output"
        mock_tool_wrapper.tool = mock_tool

        with patch.object(
            service, "create_tool_instance", return_value=mock_tool_wrapper
        ):
            result = await service.execute_tool(
                "test_tool", "input_data", {"config": "value"}
            )

        assert result == "formatted_output"
        mock_tool_wrapper.format_input.assert_called_once_with("input_data")
        mock_tool.ainvoke.assert_called_once_with("formatted_input")
        mock_tool_wrapper.format_output.assert_called_once_with("raw_output")

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execute_tool_with_error(self, mock_tool_service_for_execution):
        """Test tool execution with error."""
        service, workflow_config = mock_tool_service_for_execution

        mock_tool_wrapper = Mock()
        mock_tool = AsyncMock()
        mock_tool.ainvoke.side_effect = Exception("Tool execution failed")
        mock_tool_wrapper.tool = mock_tool
        mock_tool_wrapper.format_input.return_value = "formatted_input"

        with patch.object(
            service, "create_tool_instance", return_value=mock_tool_wrapper
        ):
            with pytest.raises(Exception, match="Tool execution failed"):
                await service.execute_tool("test_tool", "input_data")


class TestToolServiceToolInformation:
    """Test tool information and listing methods."""

    @pytest.fixture(scope="function")
    def mock_tool_service_with_tool_info(self):
        """Create mock tool service with tool information."""
        workflow_config = Mock(spec=WorkflowConfig)

        # Mock tools
        mock_tool1 = Mock()
        mock_tool1.name = "tool1"
        mock_tool2 = Mock()
        mock_tool2.name = "tool2"
        mock_tool3 = Mock()
        mock_tool3.name = "tool3"

        workflow_config.validated_tools = [mock_tool1, mock_tool2, mock_tool3]
        workflow_config.activated_tools = [mock_tool1, mock_tool2]

        service = ToolService(workflow_config)
        return service, workflow_config, [mock_tool1, mock_tool2, mock_tool3]

    def test_collect_tools_info(self, mock_tool_service_with_tool_info):
        """Test collecting tools information."""
        service, workflow_config, tools = mock_tool_service_with_tool_info

        with patch(
            "quivr_core.rag.langgraph_framework.services.tool_service.collect_tools"
        ) as mock_collect:
            mock_collect.return_value = ("validated_info", "activated_info")

            validated_info, activated_info = service.collect_tools_info()

        assert validated_info == "validated_info"
        assert activated_info == "activated_info"
        mock_collect.assert_called_once_with(workflow_config)

    def test_get_tool_by_name_found(self, mock_tool_service_with_tool_info):
        """Test getting tool by name when found."""
        service, workflow_config, tools = mock_tool_service_with_tool_info

        result = service.get_tool_by_name("tool2")

        assert result == tools[1]

    def test_get_tool_by_name_not_found(self, mock_tool_service_with_tool_info):
        """Test getting tool by name when not found."""
        service, workflow_config, tools = mock_tool_service_with_tool_info

        result = service.get_tool_by_name("nonexistent_tool")

        assert result is None

    def test_list_available_tools(self, mock_tool_service_with_tool_info):
        """Test listing available tool names."""
        service, workflow_config, tools = mock_tool_service_with_tool_info

        result = service.list_available_tools()

        assert result == ["tool1", "tool2", "tool3"]

    def test_list_activated_tools(self, mock_tool_service_with_tool_info):
        """Test listing activated tool names."""
        service, workflow_config, tools = mock_tool_service_with_tool_info

        result = service.list_activated_tools()

        assert result == ["tool1", "tool2"]


class TestToolServiceConfigurationManagement:
    """Test workflow configuration management."""

    def test_get_workflow_config(self):
        """Test getting workflow configuration."""
        workflow_config = WorkflowConfig()
        service = ToolService(workflow_config)

        result = service.get_workflow_config()

        assert result == workflow_config
        assert result is workflow_config  # Same object reference

    def test_update_workflow_config(self):
        """Test updating workflow configuration."""
        old_config = WorkflowConfig(name="old_config")
        service = ToolService(old_config)

        new_config = WorkflowConfig(name="new_config")
        service.update_workflow_config(new_config)

        # Test that the configuration was actually updated
        assert service.workflow_config is new_config
        assert service.workflow_config is not old_config
        assert service.workflow_config.name == "new_config"

    def test_update_workflow_config_with_different_attributes(self):
        """Test updating workflow configuration with different attributes."""
        # Create configs with different attributes to ensure they're different
        old_config = WorkflowConfig()
        old_config.name = "original"

        service = ToolService(old_config)

        new_config = WorkflowConfig()
        new_config.name = "updated"

        service.update_workflow_config(new_config)

        # Verify the update worked
        assert service.workflow_config.name == "updated"
        assert service.workflow_config is new_config
        assert old_config.name == "original"  # Original unchanged
