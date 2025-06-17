"""Tests for the service container and dependency injection system."""

import pytest

from quivr_core.rag.entities.config import LLMEndpointConfig, WorkflowConfig
from quivr_core.rag.langgraph_framework.services.service_container import (
    ServiceContainer,
    ServiceFactory,
    LLMServiceFactory,
    ToolServiceFactory,
    PromptServiceFactory,
)
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.services.tool_service import ToolService
from quivr_core.rag.langgraph_framework.services.rag_prompt_service import (
    RAGPromptService,
)

from tests.rag.langgraph_framework.fixtures.mock_services import (
    MockLLMService,
    MockServiceFactory,
)


class TestServiceFactory:
    """Test ServiceFactory abstract base class."""

    def test_service_factory_is_abstract(self):
        """Test that ServiceFactory cannot be instantiated directly."""
        with pytest.raises(TypeError):
            ServiceFactory()


class TestLLMServiceFactory:
    """Test LLMServiceFactory."""

    def test_create_with_default_config(self):
        """Test creating LLM service with default config."""
        factory = LLMServiceFactory()
        service = factory.create()

        assert isinstance(service, LLMService)
        assert isinstance(service.config, LLMEndpointConfig)

    def test_create_with_custom_config(self):
        """Test creating LLM service with custom config."""
        factory = LLMServiceFactory()
        config = LLMEndpointConfig(
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_context_tokens=10000,
            max_output_tokens=5000,
        )
        service = factory.create(config)

        assert isinstance(service, LLMService)
        assert service.config.model == "gpt-3.5-turbo"
        assert service.config.temperature == 0.5

    def test_get_config_type(self):
        """Test getting config type."""
        factory = LLMServiceFactory()
        assert factory.get_config_type() == LLMEndpointConfig


class TestToolServiceFactory:
    """Test ToolServiceFactory."""

    def test_create_with_default_config(self):
        """Test creating tool service with default config."""
        factory = ToolServiceFactory()
        service = factory.create()

        assert isinstance(service, ToolService)
        assert isinstance(service.workflow_config, WorkflowConfig)

    def test_create_with_custom_config(self):
        """Test creating tool service with custom config."""
        factory = ToolServiceFactory()
        config = WorkflowConfig()  # Use default but ensure it's a proper instance
        service = factory.create(config)

        assert isinstance(service, ToolService)
        assert service.workflow_config == config

    def test_get_config_type(self):
        """Test getting config type."""
        factory = ToolServiceFactory()
        assert factory.get_config_type() == WorkflowConfig


class TestPromptServiceFactory:
    """Test PromptServiceFactory."""

    def test_create_service(self):
        """Test creating prompt service."""
        factory = PromptServiceFactory()
        service = factory.create()

        assert isinstance(service, RAGPromptService)

    def test_create_with_config_ignored(self):
        """Test that config is ignored for prompt service."""
        factory = PromptServiceFactory()
        service = factory.create("ignored_config")

        assert isinstance(service, RAGPromptService)

    def test_get_config_type_none(self):
        """Test that config type is None."""
        factory = PromptServiceFactory()
        assert factory.get_config_type() is None


class TestServiceContainer:
    """Test ServiceContainer dependency injection."""

    @pytest.fixture(scope="function")
    def container(self):
        """Create a fresh service container."""
        return ServiceContainer()

    def test_container_initialization(self, container):
        """Test container initializes with default factories."""
        assert LLMService in container._factories
        assert ToolService in container._factories
        assert RAGPromptService in container._factories

        assert isinstance(container._factories[LLMService], LLMServiceFactory)
        assert isinstance(container._factories[ToolService], ToolServiceFactory)
        assert isinstance(container._factories[RAGPromptService], PromptServiceFactory)

    def test_register_custom_factory(self, container):
        """Test registering a custom factory."""
        mock_service = MockLLMService()
        factory = MockServiceFactory(mock_service)

        container.register_factory(MockLLMService, factory)

        assert MockLLMService in container._factories
        assert container._factories[MockLLMService] == factory

    def test_get_singleton_service(self, container):
        """Test getting singleton service without config."""
        service1 = container.get_service(RAGPromptService)
        service2 = container.get_service(RAGPromptService)

        # Should be the same instance (singleton)
        assert service1 is service2
        assert isinstance(service1, RAGPromptService)

    def test_get_service_with_config(self, container):
        """Test getting service with configuration."""
        config = LLMEndpointConfig(
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_context_tokens=10000,
            max_output_tokens=5000,
        )
        service = container.get_service(LLMService, config)

        assert isinstance(service, LLMService)
        assert service.config.model == "gpt-3.5-turbo"
        assert service.config.temperature == 0.7

    def test_config_change_detection(self, container):
        """Test that config changes create new service instances."""
        config1 = LLMEndpointConfig(
            model="gpt-3.5-turbo",
            temperature=0.5,
            max_context_tokens=10000,
            max_output_tokens=5000,
        )
        config2 = LLMEndpointConfig(
            model="gpt-4",
            temperature=0.7,
            max_context_tokens=10000,
            max_output_tokens=5000,
        )

        service1 = container.get_service(LLMService, config1)
        service2 = container.get_service(LLMService, config2)

        # Should be different instances due to different configs
        assert service1 is not service2
        assert service1.config.model == "gpt-3.5-turbo"
        assert service2.config.model == "gpt-4"

    def test_same_config_returns_cached_service(self, container):
        """Test that same config returns cached service."""
        config = LLMEndpointConfig(
            model="gpt-4",
            temperature=0.7,
            max_context_tokens=10000,
            max_output_tokens=5000,
        )

        service1 = container.get_service(LLMService, config)
        service2 = container.get_service(LLMService, config)

        # Should be the same instance (cached)
        assert service1 is service2

    def test_config_hash_calculation(self, container):
        """Test that config hashing works correctly."""
        config1 = LLMEndpointConfig(
            model="gpt-4",
            temperature=0.7,
            max_context_tokens=10000,
            max_output_tokens=5000,
        )
        config2 = LLMEndpointConfig(
            model="gpt-4",
            temperature=0.7,
            max_context_tokens=10000,
            max_output_tokens=5000,
        )  # Same values
        config3 = LLMEndpointConfig(
            model="gpt-4",
            temperature=0.8,  # Different value
            max_context_tokens=10000,
            max_output_tokens=5000,
        )

        service1 = container.get_service(LLMService, config1)
        service2 = container.get_service(LLMService, config2)
        service3 = container.get_service(LLMService, config3)

        # Same config values should return same instance
        assert service1 is service2
        # Different config should return different instance
        assert service1 is not service3

    def test_invalid_service_type(self, container):
        """Test error for unregistered service type."""

        class UnregisteredService:
            pass

        with pytest.raises(ValueError, match="No factory registered for service type"):
            container.get_service(UnregisteredService)

    def test_invalid_config_type(self, container):
        """Test error for invalid config type."""
        # Try to use WorkflowConfig for LLMService (wrong config type)
        wrong_config = WorkflowConfig()

        with pytest.raises(TypeError, match="Expected config of type"):
            container.get_service(LLMService, wrong_config)

    def test_clear_cache(self, container):
        """Test clearing service cache."""
        # Create some cached services
        service1 = container.get_service(RAGPromptService)
        config = LLMEndpointConfig(
            model="gpt-4", max_context_tokens=10000, max_output_tokens=5000
        )
        service2 = container.get_service(LLMService, config)

        # Clear cache
        container.clear_cache()

        # Should create new instances
        service3 = container.get_service(RAGPromptService)
        service4 = container.get_service(LLMService, config)

        assert service1 is not service3
        assert service2 is not service4

    def test_config_with_non_pydantic_model(self, container):
        """Test config handling with non-Pydantic objects."""
        mock_service = MockLLMService()
        factory = MockServiceFactory(mock_service, config_type=None)
        container.register_factory(MockLLMService, factory)

        # Use string config (non-Pydantic)
        config = "string_config"
        service1 = container.get_service(MockLLMService, config)
        service2 = container.get_service(MockLLMService, config)

        # Should cache based on string representation
        assert service1 is service2

    def test_service_creation_logging(self, container, caplog):
        """Test that service creation is logged."""
        container.get_service(RAGPromptService)

        assert "Creating singleton instance of RAGPromptService" in caplog.text

    def test_factory_config_type_validation_skip(self, container):
        """Test that config type validation can be skipped for factories without config types."""
        # RAGPromptService factory has no config type, so any config should be accepted
        service = container.get_service(RAGPromptService, "any_config")
        assert isinstance(service, RAGPromptService)
