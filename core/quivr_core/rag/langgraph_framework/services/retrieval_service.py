import logging
import hashlib
import json
from typing import Optional
from langchain_core.vectorstores import VectorStore
from langchain_core.vectorstores import VectorStoreRetriever
from langchain.retrievers import ContextualCompressionRetriever

from quivr_core.rag.langgraph_framework.entities.retrieval_service_config import (
    RetrievalServiceConfig,
)
from quivr_core.rag.langgraph_framework.services.utils import (
    get_retriever,
    get_compression_retriever,
)

logger = logging.getLogger("quivr_core")


class RetrievalService:
    """Service for creating and managing retrievers with vector store dependency."""

    def __init__(self, config: RetrievalServiceConfig, vector_store: VectorStore):
        self.config = config
        self.vector_store = vector_store

        # Cache for retrievers
        self._basic_retriever: Optional[VectorStoreRetriever] = None
        self._compression_retriever: Optional[ContextualCompressionRetriever] = None

        # Configuration hashes for cache invalidation
        self._basic_retriever_config_hash: Optional[str] = None
        self._compression_retriever_config_hash: Optional[str] = None

    def _compute_config_hash(self, *configs) -> str:
        """Compute hash of configuration objects for cache invalidation."""
        config_data = []
        for config in configs:
            if hasattr(config, "model_dump"):
                config_data.append(config.model_dump())
            else:
                config_data.append(str(config))

        return hashlib.md5(json.dumps(config_data, sort_keys=True).encode()).hexdigest()

    def get_basic_retriever(self, use_cache: bool = True) -> VectorStoreRetriever:
        """
        Get a basic vector store retriever with caching.

        Returns:
            VectorStoreRetriever instance
        """
        # Compute hash of current retriever config
        current_hash = self._compute_config_hash(self.config.retriever_config)

        # Check if we need to recreate the retriever
        if (
            self._basic_retriever is None
            or self._basic_retriever_config_hash != current_hash
            or not use_cache
        ):
            logger.debug("Creating new basic retriever")
            self._basic_retriever = get_retriever(
                self.vector_store, self.config.retriever_config
            )
            self._basic_retriever_config_hash = current_hash
        else:
            logger.debug("Using cached basic retriever")

        return self._basic_retriever

    def get_compression_retriever(self) -> ContextualCompressionRetriever:
        """
        Get a compression retriever with reranking and caching.

        Returns:
            ContextualCompressionRetriever instance
        """
        # Compute hash of current retriever and reranker configs
        current_hash = self._compute_config_hash(
            self.config.retriever_config, self.config.reranker_config
        )

        # Check if we need to recreate the compression retriever
        if (
            self._compression_retriever is None
            or self._compression_retriever_config_hash != current_hash
        ):
            logger.debug("Creating new compression retriever")
            self._compression_retriever = get_compression_retriever(
                self.vector_store,
                self.config.retriever_config,
                self.config.reranker_config,
            )
            self._compression_retriever_config_hash = current_hash
        else:
            logger.debug("Using cached compression retriever")

        return self._compression_retriever

    def get_vector_store(self) -> VectorStore:
        """Get the underlying vector store."""
        return self.vector_store

    def clear_cache(self):
        """Clear all cached retrievers."""
        logger.debug("Clearing retrieval service cache")
        self._basic_retriever = None
        self._compression_retriever = None
        self._basic_retriever_config_hash = None
        self._compression_retriever_config_hash = None

    def update_config(self, new_config: RetrievalServiceConfig):
        """
        Update the service configuration and invalidate cache if needed.

        Args:
            new_config: New retrieval service configuration
        """
        # Check if config actually changed
        if hasattr(self.config, "model_dump") and hasattr(new_config, "model_dump"):
            if self.config.model_dump() != new_config.model_dump():
                logger.debug("Configuration changed, clearing cache")
                self.clear_cache()
        else:
            # Fallback comparison
            if str(self.config) != str(new_config):
                logger.debug("Configuration changed, clearing cache")
                self.clear_cache()

        self.config = new_config
