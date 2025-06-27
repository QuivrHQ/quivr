"""Tests for the BaseNode abstract class and core functionality."""

import pytest
from unittest.mock import Mock

from quivr_core.rag.langgraph_framework.base.node import BaseNode
from quivr_core.rag.langgraph_framework.base.exceptions import NodeValidationError
from quivr_core.rag.langgraph_framework.base.extractors import ConfigExtractor
from quivr_core.rag.langgraph_framework.services.service_container import (
    ServiceContainer,
)

from tests.rag.langgraph_framework.fixtures.mock_nodes import (
    MockNode,
    FailingMockNode,
    AsyncMockNode,
    ValidationErrorMockNode,
    MockConfig,
)
from tests.rag.langgraph_framework.fixtures.mock_services import MockLLMService


class TestBaseNodeInitialization:
    """Test BaseNode initialization and basic properties."""

    def test_node_initialization_defaults(self):
        """Test node initialization with default values."""
        node = MockNode()

        assert node.node_name == "mock_node"
        assert node.name == "mock_node"
        assert node.config_extractor is None
        assert isinstance(node.service_container, ServiceContainer)
        assert node._config_hashes == {}

    def test_node_initialization_with_custom_name(self):
        """Test node initialization with custom name."""
        node = MockNode(node_name="custom_name")

        assert node.node_name == "custom_name"
        assert node.name == "custom_name"

    def test_node_initialization_with_config_extractor(self):
        """Test node initialization with config extractor."""
        extractor = Mock(spec=ConfigExtractor)
        node = MockNode(config_extractor=extractor)

        assert node.config_extractor is extractor

    def test_node_initialization_with_service_container(self):
        """Test node initialization with custom service container."""
        container = Mock(spec=ServiceContainer)
        node = MockNode(service_container=container)

        assert node.service_container is container


class TestBaseNodeConfigExtraction:
    """Test configuration extraction and caching."""

    @pytest.fixture(scope="function")
    def mock_extractor(self):
        """Create a mock config extractor."""
        extractor = Mock(spec=ConfigExtractor)
        return extractor

    def test_get_config_without_extractor(self):
        """Test config extraction without extractor returns defaults."""
        node = MockNode()

        config = node.get_config(MockConfig)

        assert isinstance(config, MockConfig)
        assert config.test_param == "default_value"
        assert config.numeric_param == 42

    def test_get_config_without_extractor_caching(self):
        """Test that default config is cached properly."""
        node = MockNode()

        config1 = node.get_config(MockConfig)
        config2 = node.get_config(MockConfig)

        assert config1 == config2

    def test_get_config_with_extractor(self, mock_extractor):
        """Test config extraction with extractor."""
        # Setup mock extractor
        expected_config = MockConfig(test_param="extracted_value", numeric_param=100)
        mock_extractor.extract.return_value = expected_config

        node = MockNode(config_extractor=mock_extractor)
        graph_config = {"test": "config"}

        config = node.get_config(MockConfig, graph_config)

        assert config == expected_config
        mock_extractor.extract.assert_called_once_with(
            graph_config, MockConfig, "mock_node"
        )

    def test_get_config_change_detection(self, mock_extractor):
        """Test config change detection."""
        # First config
        config1 = MockConfig(test_param="value1", numeric_param=1)
        mock_extractor.extract.return_value = config1

        node = MockNode(config_extractor=mock_extractor)
        graph_config = {"test": "config"}

        extracted1 = node.get_config(MockConfig, graph_config)
        assert extracted1 == config1

        # Same config (no change)
        extracted2 = node.get_config(MockConfig, graph_config)
        assert extracted2 == config1

        # Different config (change detected)
        config2 = MockConfig(test_param="value2", numeric_param=2)
        mock_extractor.extract.return_value = config2

        extracted3 = node.get_config(MockConfig, graph_config)
        assert extracted3 == config2

    def test_get_config_node_specific_caching(self, mock_extractor):
        """Test that config caching is node-specific."""
        config = MockConfig(test_param="test", numeric_param=1)
        mock_extractor.extract.return_value = config

        node1 = MockNode(node_name="node1", config_extractor=mock_extractor)
        node2 = MockNode(node_name="node2", config_extractor=mock_extractor)

        graph_config = {"test": "config"}

        # Both nodes should detect change on first call
        config1 = node1.get_config(MockConfig, graph_config)
        config2 = node2.get_config(MockConfig, graph_config)

        assert config1 == config
        assert config2 == config

        # Cache should be separate for each node
        cache_key1 = (MockConfig, "node1")
        cache_key2 = (MockConfig, "node2")

        assert cache_key1 in node1._config_hashes
        assert cache_key2 in node2._config_hashes


class TestBaseNodeServiceInjection:
    """Test service injection functionality."""

    def test_get_service_basic(self):
        """Test basic service retrieval."""
        mock_container = Mock(spec=ServiceContainer)
        mock_service = MockLLMService()
        mock_container.get_service.return_value = mock_service

        node = MockNode(service_container=mock_container)
        service = node.get_service(MockLLMService)

        assert service is mock_service
        mock_container.get_service.assert_called_once_with(MockLLMService, None)

    def test_get_service_with_config(self):
        """Test service retrieval with config."""
        mock_container = Mock(spec=ServiceContainer)
        mock_service = MockLLMService()
        mock_container.get_service.return_value = mock_service

        node = MockNode(service_container=mock_container)
        config = {"test": "config"}
        service = node.get_service(MockLLMService, config)

        assert service is mock_service
        mock_container.get_service.assert_called_once_with(MockLLMService, config)


class TestBaseNodeValidation:
    """Test input/output validation."""

    def test_abstract_validation_methods(self):
        """Test that validation methods are abstract and must be implemented."""
        # MockNode implements these, so we need to test with a truly abstract case
        with pytest.raises(TypeError):
            # This should fail because BaseNode is abstract
            BaseNode()


class TestBaseNodeErrorHandling:
    """Test error handling functionality."""

    def test_handle_error_with_dict_state(self):
        """Test error handling with dictionary state."""
        node = MockNode()
        error = ValueError("Test error")
        state = {"key": "value"}

        result = node.handle_error(error, state)

        assert result["key"] == "value"
        assert result["error"] == "Error in mock_node: Test error"
        assert result["node_error"] == "mock_node"

    def test_handle_error_with_state_with_error_method(self):
        """Test error handling with state that has with_error method."""
        node = MockNode()
        error = ValueError("Test error")

        # Mock state with with_error method
        mock_state = Mock()
        mock_state.with_error.return_value = "error_state"

        result = node.handle_error(error, mock_state)

        assert result == "error_state"
        mock_state.with_error.assert_called_once_with("Error in mock_node: Test error")

    def test_handle_error_with_unsupported_state(self, caplog):
        """Test error handling with unsupported state type."""
        node = MockNode()
        error = ValueError("Test error")
        state = "unsupported_state_type"

        result = node.handle_error(error, state)

        assert result == state  # Should return unchanged
        assert "Could not add error info to state" in caplog.text


class TestBaseNodeExecution:
    """Test node execution lifecycle."""

    @pytest.mark.asyncio(loop_scope="session")
    async def test_successful_execution(self):
        """Test successful node execution."""
        node = MockNode()
        state = {"input": "test"}
        config = {"config": "test"}

        result = await node(state, config)

        assert node.executed is True
        assert node.execution_count == 1
        assert node.last_state == state
        assert node.last_config == config
        assert result["processed_by"] == "mock_node"

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execution_with_input_validation_error(self):
        """Test execution with input validation error raises exception."""
        node = MockNode()
        state = {"invalid_input": True}  # This will trigger validation error

        with pytest.raises(ValueError, match="Invalid input state"):
            await node(state)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execution_with_output_validation_error(self):
        """Test execution with output validation error raises exception."""
        node = MockNode()
        state = {"invalid_output": True}  # This will trigger output validation error

        with pytest.raises(ValueError, match="Invalid output state"):
            await node(state)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execution_with_node_validation_error(self):
        """Test that NodeValidationError is raised."""
        node = ValidationErrorMockNode()
        state = {"validation_error": True}  # This will trigger NodeValidationError

        with pytest.raises(NodeValidationError, match="Validation failed"):
            await node(state)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execution_with_general_error(self):
        """Test execution with general error raises exception."""
        node = FailingMockNode()
        state = {"input": "test"}

        with pytest.raises(RuntimeError, match="Mock execution failure"):
            await node(state)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_async_execution(self):
        """Test async node execution."""
        node = AsyncMockNode()
        state = {"input": "test"}

        result = await node(state)

        assert node.async_executed is True
        assert result["async_result"] is True

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execution_logging(self, caplog):
        """Test that execution is logged."""
        node = MockNode()
        state = {"input": "test"}

        await node(state)

        assert "Executing mock_node" in caplog.text
        assert "Completed mock_node" in caplog.text

    @pytest.mark.asyncio(loop_scope="session")
    async def test_execution_error_logging(self, caplog):
        """Test that execution errors are logged."""
        node = FailingMockNode()
        state = {"input": "test"}

        with pytest.raises(RuntimeError):
            await node(state)

        assert "Error in failing_mock_node: Mock execution failure" in caplog.text


class TestBaseNodeMetadata:
    """Test node metadata handling."""

    def test_node_metadata_attribute(self):
        """Test that nodes can have metadata attribute."""
        _ = MockNode()

        # Should have NODE_NAME
        assert hasattr(MockNode, "NODE_NAME")
        assert MockNode.NODE_NAME == "mock_node"

    def test_node_metadata_optional(self):
        """Test that _node_metadata is optional."""
        _ = MockNode()

        # _node_metadata might not exist, and that's okay
        metadata = getattr(MockNode, "_node_metadata", None)
        # Should be None or a dict if it exists
        assert metadata is None or isinstance(metadata, dict)
