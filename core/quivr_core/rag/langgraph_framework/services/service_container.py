from typing import Dict, Type, TypeVar, Any, Optional
from abc import ABC, abstractmethod
import logging
from quivr_core.rag.entities.config import LLMEndpointConfig, WorkflowConfig
from quivr_core.rag.langgraph_framework.entities.retrieval_service_config import (
    RetrievalServiceConfig,
)
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.rag.langgraph_framework.services.tool_service import ToolService
from quivr_core.rag.langgraph_framework.services.rag_prompt_service import (
    RAGPromptService,
)
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


class PromptServiceFactory(ServiceFactory):
    def create(self, config: Optional[Any] = None) -> RAGPromptService:
        return RAGPromptService()

    def get_config_type(self) -> Optional[Type]:
        return None


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
    """Dependency injection container for services."""

    def __init__(self, vector_store=None):
        self._services: Dict[tuple, Any] = {}  # Changed to support tuple keys
        self._factories: Dict[Type, ServiceFactory] = {
            LLMService: LLMServiceFactory(),
            ToolService: ToolServiceFactory(),
            RAGPromptService: PromptServiceFactory(),
        }

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

    def get_service(self, service_type: Type[T], config: Optional[Any] = None) -> T:
        """Get or create a service instance with config change detection."""
        import hashlib
        import json

        # If no config is provided, use singleton pattern
        if config is None:
            cache_key = (service_type, "singleton")
            if cache_key not in self._services:
                if service_type not in self._factories:
                    raise ValueError(
                        f"No factory registered for service type: {service_type}"
                    )

                factory = self._factories[service_type]
                logger.debug(f"Creating singleton instance of {service_type.__name__}")
                service = factory.create(None)
                self._services[cache_key] = service

            return self._services[cache_key]

        # Create config hash for change detection when config is provided
        config_dict = (
            config.model_dump() if hasattr(config, "model_dump") else str(config)
        )
        config_hash = hashlib.md5(
            json.dumps(config_dict, sort_keys=True).encode()
        ).hexdigest()

        # Check if we need to recreate the service
        cache_key = (service_type, config_hash)
        if (
            cache_key not in self._services
            or self._config_hashes.get(service_type) != config_hash
        ):
            if service_type not in self._factories:
                raise ValueError(
                    f"No factory registered for service type: {service_type}"
                )

            factory = self._factories[service_type]

            # Validate config type (skip validation if factory doesn't specify a config type)
            expected_config_type = factory.get_config_type()
            if expected_config_type is not None and not isinstance(
                config, expected_config_type
            ):
                raise TypeError(
                    f"Expected config of type {expected_config_type}, got {type(config)}"
                )

            logger.debug(f"Creating new instance of {service_type.__name__}")
            service = factory.create(config)
            self._services[cache_key] = service
            self._config_hashes[service_type] = config_hash

        return self._services[cache_key]

    def clear_cache(self):
        """Clear all cached services."""
        self._services.clear()
        self._config_hashes.clear()
