"""
Configuration extraction interfaces and implementations.
Allows nodes to receive config extractors that know how to navigate different config structures.
"""

from typing import Dict, Any, Type, Union, Callable
from quivr_core.rag.langgraph_framework.nodes.base.exceptions import (
    ConfigExtractionError,
)
from quivr_core.rag.langgraph_framework.nodes.base.graph_config import BaseGraphConfig
from pydantic import BaseModel


class ConfigMapping:
    """
    Type-safe configuration mapping that maps config types to extraction logic.

    Usage:
        ConfigMapping({
            PromptConfig: "prompt_config",
            LLMEndpointConfig: "llm_config",
            WorkflowConfig: lambda config: config.get("workflow", {})
        })
    """

    def __init__(
        self,
        mapping: Dict[
            Type[BaseModel], Union[str, Callable[[BaseGraphConfig], Dict[str, Any]]]
        ],
    ):
        self.mapping = mapping

    def extract(
        self, config: BaseGraphConfig, config_type: Type[BaseModel]
    ) -> BaseModel:
        """Extract and validate a specific config type."""

        try:
            extractor = self.mapping.get(config_type)

            if extractor is None:
                # Return default instance if not mapped
                return config_type()

            if isinstance(extractor, str):
                # Simple key extraction
                config_dict = config.get(extractor, {})
            elif callable(extractor):
                # Custom extraction function
                config_dict = extractor(config)
            else:
                raise ValueError(f"Invalid extractor for {config_type}: {extractor}")

            return config_type.model_validate(config_dict)
        except Exception as e:
            raise ConfigExtractionError(f"Error extracting {config_type}: {e}") from e

    def extract_all(self, config: BaseGraphConfig, config_types: tuple) -> tuple:
        """Extract all config types in the specified order."""
        return tuple(self.extract(config, config_type) for config_type in config_types)


# For convenience
ConfigExtractor = ConfigMapping
