"""
Configuration extraction interfaces and implementations.
Allows nodes to receive config extractors that know how to navigate different config structures.
"""

from typing import Dict, Any, Type, Union, Callable, Optional
from quivr_core.rag.langgraph_framework.nodes.base.exceptions import (
    ConfigExtractionError,
)
from quivr_core.rag.langgraph_framework.nodes.base.graph_config import BaseGraphConfig
from pydantic import BaseModel
import copy


class ConfigMapping:
    """
    Type-safe configuration mapping that maps config types to extraction logic.
    Supports node-specific config overrides with global fallbacks.

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
        self,
        config: BaseGraphConfig,
        config_type: Type[BaseModel],
        node_name: Optional[str] = None,
    ) -> BaseModel:
        """Extract and validate a specific config type with optional node-specific overrides."""

        try:
            # 1. Extract global config as base
            global_config_dict = self._extract_global_config(config, config_type)

            # 2. If no node name provided, return global config
            if not node_name:
                return config_type.model_validate(global_config_dict)

            # 3. Look for node-specific overrides
            node_config_dict = self._extract_node_config(config, config_type, node_name)

            # 4. Merge node config over global config (deep merge)
            merged_config_dict = self._deep_merge(global_config_dict, node_config_dict)

            return config_type.model_validate(merged_config_dict)

        except Exception as e:
            raise ConfigExtractionError(
                f"Error extracting {config_type} for node {node_name}: {e}"
            ) from e

    def _extract_global_config(
        self, config: BaseGraphConfig, config_type: Type[BaseModel]
    ) -> Dict[str, Any]:
        """Extract global config using the mapping."""
        extractor = self.mapping.get(config_type)

        if extractor is None:
            # Return empty dict if not mapped - will create default instance
            return {}

        if isinstance(extractor, str):
            # Simple key extraction
            return config.get(extractor, {})
        elif callable(extractor):
            # Custom extraction function
            return extractor(config)
        else:
            raise ValueError(f"Invalid extractor for {config_type}: {extractor}")

    def _extract_node_config(
        self, config: BaseGraphConfig, config_type: Type[BaseModel], node_name: str
    ) -> Dict[str, Any]:
        """Extract node-specific config overrides."""
        # Convention: nodes.{node_name}.{config_key}
        nodes_config = config.get("nodes", {})
        node_config = nodes_config.get(node_name, {})

        # Get the config key for this type
        extractor = self.mapping.get(config_type)
        if isinstance(extractor, str):
            config_key = extractor
        else:
            # For callable extractors, use the type name in snake_case
            config_key = self._type_to_snake_case(config_type.__name__)

        return node_config.get(config_key, {})

    def _deep_merge(
        self, base: Dict[str, Any], override: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deep merge two dictionaries, with override taking precedence."""
        result = copy.deepcopy(base)

        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                # Recursively merge nested dictionaries
                result[key] = self._deep_merge(result[key], value)
            else:
                # Override the value
                result[key] = value

        return result

    def _type_to_snake_case(self, type_name: str) -> str:
        """Convert PascalCase to snake_case."""
        result = []
        for i, char in enumerate(type_name):
            if char.isupper() and i > 0:
                result.append("_")
            result.append(char.lower())
        return "".join(result)

    def extract_all(
        self,
        config: BaseGraphConfig,
        config_types: tuple,
        node_name: Optional[str] = None,
    ) -> tuple:
        """Extract all config types in the specified order."""
        return tuple(
            self.extract(config, config_type, node_name) for config_type in config_types
        )


# For convenience
ConfigExtractor = ConfigMapping
