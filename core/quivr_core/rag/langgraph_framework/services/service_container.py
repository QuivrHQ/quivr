from typing import Dict, Type, TypeVar, Any, Optional
from abc import ABC, abstractmethod
import logging
from collections import OrderedDict as OrderedDictImpl
from quivr_core.rag.entities.config import LLMEndpointConfig, WorkflowConfig
from quivr_core.rag.langgraph_framework.entities.retrieval_service_config import (
    RetrievalServiceConfig,
)
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.services.tool_service import ToolService

from quivr_core.rag.langgraph_framework.services.retrieval_service import (
    RetrievalService,
)

logger = logging.getLogger("quivr_core")

T = TypeVar("T")


class ServiceFactory(ABC):
    """Abstract factory for creating services."""

    @abstractmethod
    def create(self, config: Optional[Any] = None) -> Any:
        pass

    @abstractmethod
    def get_config_type(self) -> Optional[Type]:
        pass


class LLMServiceFactory(ServiceFactory):
    def create(self, config: Optional[LLMEndpointConfig] = None) -> LLMService:
        if config is None:
            config = LLMEndpointConfig()  # Use default config
        return LLMService(llm_config=config)

    def get_config_type(self) -> Type[LLMEndpointConfig]:
        return LLMEndpointConfig


class ToolServiceFactory(ServiceFactory):
    def create(self, config: Optional[WorkflowConfig] = None) -> ToolService:
        if config is None:
            config = WorkflowConfig()  # Use default config
        return ToolService(workflow_config=config)

    def get_config_type(self) -> Type[WorkflowConfig]:
        return WorkflowConfig


class RetrievalServiceFactory(ServiceFactory):
    """Factory for creating retrieval services with vector store dependency."""

    def __init__(self, vector_store):
        self.vector_store = vector_store

    def create(
        self, config: Optional[RetrievalServiceConfig] = None
    ) -> RetrievalService:
        if config is None:
            config = RetrievalServiceConfig()
        return RetrievalService(config, self.vector_store)

    def get_config_type(self) -> Optional[Type]:
        return None


class ServiceContainer:
    """Dependency injection container for services with LRU cache per service type."""

    def __init__(self, vector_store=None, max_cache_per_service: int = 5):
        # Use OrderedDict for LRU cache behavior per service type
        self._services: Dict[Type, OrderedDictImpl[str, Any]] = {}
        self._factories: Dict[Type, ServiceFactory] = {
            LLMService: LLMServiceFactory(),
            ToolService: ToolServiceFactory(),
        }
        self._max_cache_per_service = max_cache_per_service

        # Register RetrieverService factory if vector_store is provided
        if vector_store:
            self._factories[RetrievalService] = RetrievalServiceFactory(vector_store)

        self._config_hashes: Dict[Type, str] = {}

    def register_factory(self, service_type: Type[T], factory: ServiceFactory):
        """Register a custom service factory."""
        self._factories[service_type] = factory

    def register_vector_store(self, vector_store):
        """Register a vector store and enable RetrievalService."""
        self._factories[RetrievalService] = RetrievalServiceFactory(vector_store)

    def _get_service_cache(self, service_type: Type) -> OrderedDictImpl[str, Any]:
        """Get or create the cache for a specific service type."""
        if service_type not in self._services:
            self._services[service_type] = OrderedDictImpl()
        return self._services[service_type]

    def _evict_oldest_if_needed(self, service_cache: OrderedDictImpl[str, Any]) -> None:
        """Remove the oldest cached service if cache is at capacity."""
        if len(service_cache) >= self._max_cache_per_service:
            oldest_key = next(iter(service_cache))
            removed_service = service_cache.pop(oldest_key)
            logger.debug(f"Evicted oldest cached service: {oldest_key}")
            # Clean up the service if it has cleanup methods
            if hasattr(removed_service, "cleanup"):
                try:
                    removed_service.cleanup()
                except Exception as e:
                    logger.warning(f"Error cleaning up evicted service: {e}")

    def get_service(
        self,
        service_type: Type[T],
        config: Optional[Any] = None,
        use_cache: bool = True,
    ) -> T:
        """
        Get or create a service instance.

        Args:
            service_type: The type of service to get.
            config: The configuration for the service.
            use_cache: If False, a new instance is created and not cached.

        Returns:
            An instance of the requested service.
        """
        import hashlib
        import json

        if service_type not in self._factories:
            raise ValueError(f"No factory registered for service type: {service_type}")

        factory = self._factories[service_type]

        # Validate config type (skip validation if factory doesn't specify a config type)
        if config is not None:
            expected_config_type = factory.get_config_type()
            if expected_config_type is not None and not isinstance(
                config, expected_config_type
            ):
                raise TypeError(
                    f"Expected config of type {expected_config_type}, got {type(config)}"
                )

        if not use_cache:
            logger.debug(f"Creating new non-cached {service_type.__name__} instance")
            return factory.create(config)

        # Get the cache for this service type
        service_cache = self._get_service_cache(service_type)

        # Determine cache key
        if config is None:
            cache_key = "singleton"
        else:
            config_dict = (
                config.model_dump() if hasattr(config, "model_dump") else str(config)
            )
            cache_key = hashlib.md5(
                json.dumps(config_dict, sort_keys=True).encode()
            ).hexdigest()

        # Check if service exists in cache
        if cache_key in service_cache:
            # Move to end (most recently used)
            service = service_cache.pop(cache_key)
            service_cache[cache_key] = service
            logger.debug(f"Retrieved cached {service_type.__name__} instance")
            return service

        # Evict oldest if at capacity
        self._evict_oldest_if_needed(service_cache)

        # Create new service
        logger.debug(f"Creating new {service_type.__name__} instance")
        service = factory.create(config)
        service_cache[cache_key] = service

        return service

    def clear_cache(self, service_type: Optional[Type] = None):
        """Clear cached services. If service_type is None, clear all caches."""
        if service_type is None:
            # Clean up all services before clearing
            for service_cache in self._services.values():
                for service in service_cache.values():
                    if hasattr(service, "cleanup"):
                        try:
                            service.cleanup()
                        except Exception as e:
                            logger.warning(
                                f"Error cleaning up service during cache clear: {e}"
                            )
            self._services.clear()
            self._config_hashes.clear()
        else:
            # Clear cache for specific service type
            if service_type in self._services:
                service_cache = self._services[service_type]
                for service in service_cache.values():
                    if hasattr(service, "cleanup"):
                        try:
                            service.cleanup()
                        except Exception as e:
                            logger.warning(
                                f"Error cleaning up {service_type.__name__} service: {e}"
                            )
                service_cache.clear()

    def get_cache_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get cache statistics for monitoring."""
        stats = {}
        for service_type, service_cache in self._services.items():
            stats[service_type.__name__] = {
                "cached_instances": len(service_cache),
                "max_capacity": self._max_cache_per_service,
                "cache_keys": list(service_cache.keys()),
            }
        return stats
