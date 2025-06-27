"""Tests for configuration extraction functionality."""

import pytest
from typing import Dict, Any
from pydantic import BaseModel

from quivr_core.rag.langgraph_framework.base.extractors import (
    ConfigMapping,
    ConfigExtractor,
)
from quivr_core.rag.langgraph_framework.base.exceptions import (
    ConfigExtractionError,
)


class TestConfig(BaseModel):
    """Test configuration model."""

    param1: str = "default1"
    param2: int = 42
    param3: bool = True


class AnotherConfig(BaseModel):
    """Another test configuration model."""

    setting1: str = "default_setting"
    setting2: float = 3.14


class TestConfigMapping:
    """Test ConfigMapping functionality."""

    def test_config_mapping_initialization(self):
        """Test ConfigMapping initialization."""
        mapping = ConfigMapping(
            {
                TestConfig: "test_config",
                AnotherConfig: lambda config: config.get("another", {}),
            }
        )

        assert TestConfig in mapping.mapping
        assert AnotherConfig in mapping.mapping
        assert mapping.mapping[TestConfig] == "test_config"
        assert callable(mapping.mapping[AnotherConfig])

    def test_extract_global_config_with_string_key(self):
        """Test extracting global config using string key."""
        mapping = ConfigMapping({TestConfig: "test_config"})

        config = {"test_config": {"param1": "test_value", "param2": 100}}

        result = mapping.extract(config, TestConfig)

        assert isinstance(result, TestConfig)
        assert result.param1 == "test_value"
        assert result.param2 == 100
        assert result.param3 is True  # Default value

    def test_extract_global_config_with_callable(self):
        """Test extracting global config using callable."""

        def custom_extractor(config):
            return config.get("custom", {})

        mapping = ConfigMapping({TestConfig: custom_extractor})

        config = {"custom": {"param1": "custom_value", "param3": False}}

        result = mapping.extract(config, TestConfig)

        assert isinstance(result, TestConfig)
        assert result.param1 == "custom_value"
        assert result.param2 == 42  # Default value
        assert result.param3 is False

    def test_extract_unmapped_config_type(self):
        """Test extracting config type that's not in mapping uses defaults."""
        mapping = ConfigMapping({})

        config = {"test_config": {"param1": "snake_case_value"}}

        result = mapping.extract(config, TestConfig)

        # Since TestConfig is not mapped, it should return defaults
        assert result.param1 == "default1"  # Fixed expectation
        assert result.param2 == 42
        assert result.param3 is True

    def test_extract_with_node_specific_overrides(self):
        """Test extracting config with node-specific overrides."""
        mapping = ConfigMapping({TestConfig: "test_config"})

        config = {
            "test_config": {"param1": "global_value", "param2": 50},
            "nodes": {"test_node": {"test_config": {"param1": "node_value"}}},
        }

        result = mapping.extract(config, TestConfig, "test_node")

        assert result.param1 == "node_value"  # Overridden
        assert result.param2 == 50  # From global
        assert result.param3 is True  # Default

    def test_extract_deep_merge_node_overrides(self):
        """Test that node overrides are deep merged with global config."""

        class NestedConfig(BaseModel):
            nested: Dict[str, Any] = {"key1": "default", "key2": "default"}
            simple: str = "default"

        mapping = ConfigMapping({NestedConfig: "nested_config"})

        config = {
            "nested_config": {
                "nested": {"key1": "global1", "key2": "global2", "key3": "global3"},
                "simple": "global_simple",
            },
            "nodes": {
                "test_node": {
                    "nested_config": {
                        "nested": {"key1": "node1"}  # Partial override
                    }
                }
            },
        }

        result = mapping.extract(config, NestedConfig, "test_node")

        assert result.nested["key1"] == "node1"  # Overridden
        assert result.nested["key2"] == "global2"  # From global
        assert result.nested["key3"] == "global3"  # From global
        assert result.simple == "global_simple"  # From global

    def test_extract_all_configs(self):
        """Test extracting all configs at once."""
        mapping = ConfigMapping(
            {TestConfig: "test_config", AnotherConfig: "another_config"}
        )

        config = {
            "test_config": {"param1": "test_value"},
            "another_config": {"setting1": "another_value"},
        }

        result = mapping.extract_all(config, (TestConfig, AnotherConfig))

        assert len(result) == 2
        assert isinstance(result[0], TestConfig)
        assert isinstance(result[1], AnotherConfig)
        assert result[0].param1 == "test_value"
        assert result[1].setting1 == "another_value"

    def test_extract_all_with_node_name(self):
        """Test extracting all configs with node-specific overrides."""
        mapping = ConfigMapping(
            {TestConfig: "test_config", AnotherConfig: "another_config"}
        )

        config = {
            "test_config": {"param1": "global_test"},
            "another_config": {"setting1": "global_another"},
            "nodes": {"test_node": {"test_config": {"param1": "node_test"}}},
        }

        result = mapping.extract_all(config, (TestConfig, AnotherConfig), "test_node")

        assert result[0].param1 == "node_test"  # Overridden
        assert result[1].setting1 == "global_another"  # Not overridden

    def test_type_to_snake_case_conversion(self):
        """Test conversion of type names to snake_case."""
        mapping = ConfigMapping({})

        assert mapping._type_to_snake_case("TestConfig") == "test_config"
        assert (
            mapping._type_to_snake_case("LLMEndpointConfig") == "l_l_m_endpoint_config"
        )
        assert mapping._type_to_snake_case("SimpleConfig") == "simple_config"
        assert mapping._type_to_snake_case("Config") == "config"

    def test_extract_with_callable_and_node_override(self):
        """Test extraction with callable extractor and node override."""

        def custom_extractor(config):
            return config.get("custom", {})

        mapping = ConfigMapping({TestConfig: custom_extractor})

        config = {
            "custom": {"param1": "global_custom"},
            "nodes": {
                "test_node": {
                    "test_config": {
                        "param1": "node_custom"
                    }  # Uses snake_case conversion
                }
            },
        }

        result = mapping.extract(config, TestConfig, "test_node")

        assert result.param1 == "node_custom"  # Node override wins

    def test_invalid_extractor_type(self):
        """Test error with invalid extractor type."""
        mapping = ConfigMapping(
            {
                TestConfig: 123  # Invalid extractor type
            }
        )

        with pytest.raises(ConfigExtractionError, match="Error extracting.*TestConfig"):
            mapping.extract({}, TestConfig)

    def test_config_extraction_error_handling(self):
        """Test error handling during config extraction."""

        def failing_extractor(config):
            raise ValueError("Extraction failed")

        mapping = ConfigMapping({TestConfig: failing_extractor})

        with pytest.raises(ConfigExtractionError, match="Error extracting.*TestConfig"):
            mapping.extract({}, TestConfig, "test_node")

    def test_pydantic_validation_error_handling(self):
        """Test handling of Pydantic validation errors."""
        mapping = ConfigMapping({TestConfig: "test_config"})

        config = {
            "test_config": {
                "param2": "not_an_integer"  # Should cause validation error
            }
        }

        with pytest.raises(ConfigExtractionError):
            mapping.extract(config, TestConfig)


class TestConfigExtractorAlias:
    """Test ConfigExtractor alias."""

    def test_config_extractor_is_config_mapping(self):
        """Test that ConfigExtractor is an alias for ConfigMapping."""
        assert ConfigExtractor is ConfigMapping

    def test_config_extractor_functionality(self):
        """Test that ConfigExtractor works the same as ConfigMapping."""
        extractor = ConfigExtractor({TestConfig: "test_config"})

        config = {"test_config": {"param1": "test_value"}}
        result = extractor.extract(config, TestConfig)

        assert isinstance(result, TestConfig)
        assert result.param1 == "test_value"


class TestConfigExtractionIntegration:
    """Test integration scenarios for config extraction."""

    def test_complex_config_hierarchy(self):
        """Test complex configuration hierarchy with multiple levels."""

        class DatabaseConfig(BaseModel):
            host: str = "localhost"
            port: int = 5432
            credentials: Dict[str, str] = {"user": "default", "password": "default"}

        class APIConfig(BaseModel):
            base_url: str = "http://localhost"
            timeout: int = 30
            headers: Dict[str, str] = {}

        mapping = ConfigMapping({DatabaseConfig: "database", APIConfig: "api"})

        config = {
            "database": {
                "host": "prod.db.com",
                "credentials": {"user": "prod_user", "password": "secret"},
            },
            "api": {
                "base_url": "https://api.prod.com",
                "headers": {"Authorization": "Bearer token"},
            },
            "nodes": {
                "db_node": {
                    "database": {
                        "port": 3306,  # Override port for this node
                        "credentials": {"user": "node_user"},  # Partial override
                    }
                },
                "api_node": {
                    "api": {
                        "timeout": 60  # Override timeout for this node
                    }
                },
            },
        }

        # Test database config for db_node
        db_config = mapping.extract(config, DatabaseConfig, "db_node")
        assert db_config.host == "prod.db.com"  # From global
        assert db_config.port == 3306  # Node override
        assert db_config.credentials["user"] == "node_user"  # Node override
        assert db_config.credentials["password"] == "secret"  # From global (deep merge)

        # Test API config for api_node
        api_config = mapping.extract(config, APIConfig, "api_node")
        assert api_config.base_url == "https://api.prod.com"  # From global
        assert api_config.timeout == 60  # Node override
        assert api_config.headers["Authorization"] == "Bearer token"  # From global

        # Test API config for different node (should use global only)
        api_config_global = mapping.extract(config, APIConfig, "other_node")
        assert api_config_global.timeout == 30  # Global default

    def test_config_extraction_with_missing_sections(self):
        """Test config extraction when some sections are missing."""
        mapping = ConfigMapping(
            {TestConfig: "test_config", AnotherConfig: "another_config"}
        )

        # Config with only one section
        config = {
            "test_config": {"param1": "test_value"}
            # another_config section is missing
        }

        # Should work and use defaults for missing sections
        test_config = mapping.extract(config, TestConfig)
        another_config = mapping.extract(config, AnotherConfig)

        assert test_config.param1 == "test_value"
        assert another_config.setting1 == "default_setting"  # Default value
