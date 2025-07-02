"""Tests for the service container and dependency injection system."""

import pytest

from quivr_core.rag.entities.config import LLMEndpointConfig, WorkflowConfig
from quivr_core.rag.langgraph_framework.services.service_container import (
    ServiceContainer,
    ServiceFactory,
    LLMServiceFactory,
    ToolServiceFactory,
)
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.services.tool_service import ToolService


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


class TestServiceContainer:
    """Test ServiceContainer dependency injection."""

    @pytest.fixture(scope="function")
    def container(self):
        """Create a fresh service container."""
        return ServiceContainer(
            max_cache_per_service=3
        )  # Use smaller cache for testing

    def test_container_initialization(self, container):
        """Test container initializes with default factories and cache settings."""
        assert LLMService in container._factories
        assert ToolService in container._factories

        assert isinstance(container._factories[LLMService], LLMServiceFactory)
        assert isinstance(container._factories[ToolService], ToolServiceFactory)

        # Test cache configuration
        assert container._max_cache_per_service == 3
        assert container._services == {}

    def test_register_custom_factory(self, container):
        """Test registering a custom factory."""
        mock_service = MockLLMService()
        factory = MockServiceFactory(mock_service)

        container.register_factory(MockLLMService, factory)

        assert MockLLMService in container._factories
        assert container._factories[MockLLMService] == factory

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

    def test_clear_all_cache(self, container):
        """Test clearing all service caches."""
        # Create some cached services
        service1 = container.get_service(LLMService)
        config = LLMEndpointConfig(
            model="gpt-4", max_context_tokens=15000, max_output_tokens=5000
        )
        service2 = container.get_service(LLMService, config)

        # Verify services are cached
        assert len(container._services) == 1
        assert LLMService in container._services

        # Clear all caches
        container.clear_cache()

        # Caches should be empty
        assert container._services == {}

        # Should create new instances
        service3 = container.get_service(LLMService)
        service4 = container.get_service(LLMService, config)

        assert service1 is not service3
        assert service2 is not service4

    def test_clear_specific_cache(self, container):
        """Test clearing cache for specific service type."""
        # Create cached services for different types
        config = LLMEndpointConfig(
            model="gpt-4", max_context_tokens=10000, max_output_tokens=5000
        )
        llm_service1 = container.get_service(LLMService, config)

        # Clear only LLMService cache
        container.clear_cache(LLMService)

        # LLMService should create new instance
        llm_service2 = container.get_service(LLMService, config)
        assert llm_service1 is not llm_service2

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
        container.get_service(LLMService)

        assert "Creating new LLMService instance" in caplog.text

    def test_service_cache_hit_logging(self, container, caplog):
        """Test that cache hits are logged."""
        # Create service first
        container.get_service(LLMService)
        caplog.clear()

        # Access again (should be cache hit)
        container.get_service(LLMService)

        assert "Retrieved cached LLMService instance" in caplog.text

    def test_lru_cache_eviction(self, container):
        """Test that LRU cache evicts oldest entries when capacity is reached."""
        # Create 4 different LLM services (cache limit is 3)
        configs = []
        services = []

        for i in range(4):
            config = LLMEndpointConfig(
                model=f"gpt-{i}",
                temperature=0.5 + i * 0.1,
                max_context_tokens=10000,
                max_output_tokens=5000,
            )
            configs.append(config)
            services.append(container.get_service(LLMService, config))

        # Should only have 3 cached services (oldest evicted)
        llm_cache = container._services[LLMService]
        assert len(llm_cache) == 3

        # When we created service 3, service 0 was evicted
        # So cache should contain services 1, 2, 3

        # Service 0 should have been evicted - requesting it creates new instance
        new_service_0 = container.get_service(LLMService, configs[0])
        assert new_service_0 is not services[0]  # New instance created

        # Now cache has evicted service 1 and contains: [2, 3, 0_new]
        # Let's verify the current cache state
        llm_cache = container._services[LLMService]
        assert len(llm_cache) == 3

        # Services 2 and 3 should still be cached
        cached_service_2 = container.get_service(LLMService, configs[2])
        cached_service_3 = container.get_service(LLMService, configs[3])

        assert cached_service_2 is services[2]
        assert cached_service_3 is services[3]

        # Service 1 should now be evicted (requesting it creates new instance)
        new_service_1 = container.get_service(LLMService, configs[1])
        assert new_service_1 is not services[1]  # New instance created

    def test_lru_cache_access_updates_order(self, container):
        """Test that accessing a cached service updates its position in LRU order."""
        # Create 3 different services to fill cache
        configs = []
        services = []

        for i in range(3):
            config = LLMEndpointConfig(
                model=f"gpt-{i}",
                temperature=0.5 + i * 0.1,
                max_context_tokens=10000,
                max_output_tokens=5000,
            )
            configs.append(config)
            services.append(container.get_service(LLMService, config))

        # Cache now contains: [0, 1, 2] in insertion order
        # Access the first service (0) to make it most recently used
        accessed_service = container.get_service(LLMService, configs[0])
        assert accessed_service is services[0]

        # Cache order is now: [1, 2, 0] (0 moved to end)

        # Add a new service, which should evict service 1 (now oldest)
        new_config = LLMEndpointConfig(
            model="gpt-new",
            temperature=0.9,
            max_context_tokens=10000,
            max_output_tokens=5000,
        )
        container.get_service(LLMService, new_config)

        # Cache order is now: [2, 0, new] (1 was evicted)

        # Service 0 should still be cached (was recently accessed)
        still_cached = container.get_service(LLMService, configs[0])
        assert still_cached is services[0]

        # Service 2 should still be cached
        cached_service_2 = container.get_service(LLMService, configs[2])
        assert cached_service_2 is services[2]

        # Service 1 should have been evicted
        evicted_service = container.get_service(LLMService, configs[1])
        assert evicted_service is not services[1]

    def test_cache_stats(self, container):
        """Test cache statistics functionality."""
        # Initially empty
        stats = container.get_cache_stats()
        assert stats == {}

        # Add some services
        container.get_service(LLMService)
        config1 = LLMEndpointConfig(
            model="gpt-4", max_context_tokens=10000, max_output_tokens=5000
        )
        config2 = LLMEndpointConfig(
            model="gpt-3.5", max_context_tokens=8000, max_output_tokens=4000
        )

        container.get_service(LLMService, config1)
        container.get_service(LLMService, config2)

        stats = container.get_cache_stats()

        assert "LLMService" in stats

        assert stats["LLMService"]["cached_instances"] == 3
        assert stats["LLMService"]["max_capacity"] == 3

        # Check cache keys are present
        assert len(stats["LLMService"]["cache_keys"]) == 3

    def test_service_cleanup_on_eviction(self, container):
        """Test that services with cleanup methods are called during eviction."""

        # Create a mock service with cleanup method
        class MockServiceWithCleanup:
            def __init__(self):
                self.cleanup_called = False

            def cleanup(self):
                self.cleanup_called = True

        class MockFactoryWithCleanup(ServiceFactory):
            def __init__(self):
                self.created_services = []

            def create(self, config=None):
                service = MockServiceWithCleanup()
                self.created_services.append(service)
                return service

            def get_config_type(self):
                return None

        # Register the mock factory
        container.register_factory(MockServiceWithCleanup, MockFactoryWithCleanup())

        # Create services to fill cache and trigger eviction
        services = []
        for i in range(4):  # One more than cache limit
            service = container.get_service(MockServiceWithCleanup, f"config_{i}")
            services.append(service)

        # First service should have been evicted and cleanup called
        factory = container._factories[MockServiceWithCleanup]
        assert factory.created_services[0].cleanup_called is True

    def test_per_service_type_cache_isolation(self, container):
        """Test that different service types have isolated caches."""
        # Fill LLMService cache
        llm_services = []
        for i in range(3):
            config = LLMEndpointConfig(
                model=f"gpt-{i}",
                temperature=0.5 + i * 0.1,
                max_context_tokens=10000,
                max_output_tokens=5000,
            )
            llm_services.append(container.get_service(LLMService, config))

        # All LLM services should still be cached
        for i, llm_service in enumerate(llm_services):
            config = LLMEndpointConfig(
                model=f"gpt-{i}",
                temperature=0.5 + i * 0.1,
                max_context_tokens=10000,
                max_output_tokens=5000,
            )
            cached_service = container.get_service(LLMService, config)
            assert cached_service is llm_service
