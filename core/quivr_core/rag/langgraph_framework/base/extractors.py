"""
Configuration extraction interfaces and implementations.
Allows nodes to receive config extractors that know how to navigate different config structures.
"""

from typing import Dict, Any, Type, Union, Callable, Optional
from quivr_core.rag.langgraph_framework.base.exceptions import (
    ConfigExtractionError,
)
from quivr_core.rag.langgraph_framework.base.graph_config import BaseGraphConfig
from pydantic import BaseModel
import copy
import logging

logger = logging.getLogger("quivr_core")


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
            Type[BaseModel], Union[str, Callable[[Dict[str, Any]], Dict[str, Any]]]
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
            _config = config.get("configurable", {})
            # 1. Extract global config as base
            global_config_dict = self._extract_global_config(_config, config_type)

            # 2. If no node name provided, return global config
            if not node_name:
                return config_type.model_validate(global_config_dict)

            # 3. Look for node-specific overrides
            node_config_dict = self._extract_node_config(
                _config, config_type, node_name
            )
            # 4. Merge node config over global config (deep merge)
            merged_config_dict = self._deep_merge(global_config_dict, node_config_dict)

            return config_type.model_validate(merged_config_dict)

        except Exception as e:
            raise ConfigExtractionError(
                f"Error extracting {config_type} for node {node_name}: {e}"
            ) from e

    def _extract_global_config(
        self, config: Dict[str, Any], config_type: Type[BaseModel]
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
        self, config: Dict[str, Any], config_type: Type[BaseModel], node_name: str
    ) -> Dict[str, Any]:
        """Enhanced to check workflow nodes AND validate configs."""
        # Standard node config lookup
        nodes_config = config.get("nodes", {})
        node_config = nodes_config.get(node_name, {})

        # Get config key
        extractor = self.mapping.get(config_type)
        if isinstance(extractor, str):
            config_key = extractor
        else:
            config_key = self._type_to_snake_case(config_type.__name__)

        node_level_config = node_config.get(config_key, {})

        # ALSO check workflow_config.nodes for node-specific configs
        workflow_config = config.get("workflow_config", {})
        workflow_nodes = workflow_config.get("nodes", [])

        for node_def in workflow_nodes:
            if node_def.get("name") == node_name:
                validated_config = node_def.get("validated_configs", {})
                workflow_node_config = validated_config.get(config_key, {})
                return self._deep_merge(workflow_node_config, node_level_config)

        return node_level_config

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
