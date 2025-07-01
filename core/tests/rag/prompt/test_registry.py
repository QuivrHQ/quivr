"""Tests for the prompt registry system."""

import pytest
from unittest.mock import Mock
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.prompts.base import BasePromptTemplate

from quivr_core.rag.prompt.registry import (
    PromptRegistry,
    PromptMetadata,
    prompt_registry,
    get_prompt,
    list_available_prompts,
    search_prompts,
)


class TestPromptMetadata:
    """Test PromptMetadata class."""

    def test_metadata_creation(self):
        """Test basic metadata creation."""
        mock_template = Mock(spec=BasePromptTemplate)
        metadata = PromptMetadata(
            prompt_template=mock_template,
            name="test_prompt",
            description="Test description",
            category="test",
            tags=["tag1", "tag2"],
        )

        assert metadata.prompt_template == mock_template
        assert metadata.name == "test_prompt"
        assert metadata.description == "Test description"
        assert metadata.category == "test"
        assert metadata.tags == ["tag1", "tag2"]

    def test_metadata_with_defaults(self):
        """Test metadata with default values."""
        mock_template = Mock(spec=BasePromptTemplate)
        metadata = PromptMetadata(prompt_template=mock_template, name="test_prompt")

        assert metadata.prompt_template == mock_template
        assert metadata.name == "test_prompt"
        assert metadata.description == ""
        assert metadata.category == "general"
        assert metadata.tags == []


class TestPromptRegistry:
    """Test PromptRegistry class."""

    def setup_method(self):
        """Setup for each test method."""
        self.registry = PromptRegistry()

    def test_registry_initialization(self):
        """Test registry initialization."""
        assert isinstance(self.registry, PromptRegistry)
        assert len(self.registry.list_items()) == 0

    def test_register_prompt_template(self):
        """Test registering a prompt template."""
        mock_template = Mock(spec=BasePromptTemplate)

        self.registry.register("test_prompt", mock_template)

        assert self.registry.has_item("test_prompt")
        assert self.registry.get("test_prompt") == mock_template

    def test_register_prompt_factory(self):
        """Test registering a prompt factory function."""
        mock_template = Mock(spec=BasePromptTemplate)
        factory = Mock(return_value=mock_template)

        self.registry.register("test_prompt", factory)

        assert self.registry.has_item("test_prompt")
        assert self.registry.get("test_prompt") == mock_template
        factory.assert_called_once()

    def test_register_prompt_factory_failure(self):
        """Test handling factory function failures."""
        factory = Mock(side_effect=Exception("Factory failed"))

        with pytest.raises(ValueError, match="Factory failed"):
            self.registry.register("test_prompt", factory)

    def test_get_nonexistent_prompt(self):
        """Test getting non-existent prompt."""
        with pytest.raises(KeyError):
            self.registry.get("nonexistent")

    def test_register_duplicate_prompt(self):
        """Test registering duplicate prompt names (should override with warning)."""
        mock_template1 = Mock(spec=BasePromptTemplate)
        mock_template2 = Mock(spec=BasePromptTemplate)

        self.registry.register("test_prompt", mock_template1)
        assert self.registry.get("test_prompt") == mock_template1

        # Should allow override (with warning logged)
        self.registry.register("test_prompt", mock_template2)
        assert self.registry.get("test_prompt") == mock_template2

    def test_unregister_prompt(self):
        """Test unregistering a prompt."""
        mock_template = Mock(spec=BasePromptTemplate)

        self.registry.register("test_prompt", mock_template)
        assert self.registry.has_item("test_prompt")

        self.registry.unregister("test_prompt")
        assert not self.registry.has_item("test_prompt")

    def test_list_prompts_by_category(self):
        """Test listing prompts by category."""
        mock_template1 = Mock(spec=BasePromptTemplate)
        mock_template2 = Mock(spec=BasePromptTemplate)
        mock_template3 = Mock(spec=BasePromptTemplate)

        self.registry.register("prompt1", mock_template1, category="cat1")
        self.registry.register("prompt2", mock_template2, category="cat2")
        self.registry.register("prompt3", mock_template3, category="cat1")

        cat1_prompts = self.registry.list_items(category="cat1")
        assert len(cat1_prompts) == 2
        assert "prompt1" in cat1_prompts
        assert "prompt3" in cat1_prompts

    def test_search_prompts(self):
        """Test searching prompts by name and description."""
        mock_template1 = Mock(spec=BasePromptTemplate)
        mock_template2 = Mock(spec=BasePromptTemplate)

        self.registry.register(
            "user_intent", mock_template1, description="Determine user intent"
        )
        self.registry.register(
            "tool_routing", mock_template2, description="Route to appropriate tools"
        )

        results = self.registry.search("intent")
        assert "user_intent" in results
        assert "tool_routing" not in results

    def test_legacy_method_names(self):
        """Test legacy method names work correctly."""
        mock_template = Mock(spec=BasePromptTemplate)

        # Test register_prompt
        self.registry.register_prompt("test_prompt", mock_template)
        assert self.registry.has_prompt("test_prompt")

        # Test get_prompt
        assert self.registry.get_prompt("test_prompt") == mock_template

        # Test get_prompt_metadata
        metadata = self.registry.get_prompt_metadata("test_prompt")
        assert isinstance(metadata, PromptMetadata)
        assert metadata.prompt_template == mock_template

        # Test list_prompts
        prompts = self.registry.list_prompts()
        assert "test_prompt" in prompts

        # Test search_prompts
        results = self.registry.search_prompts("test")
        assert "test_prompt" in results

        # Test unregister_prompt
        self.registry.unregister_prompt("test_prompt")
        assert not self.registry.has_prompt("test_prompt")


class TestRegistryDecorator:
    """Test the registry decorator."""

    def setup_method(self):
        """Setup for each test method."""
        from quivr_core.registry_base import create_registry_decorator

        self.registry = PromptRegistry()
        self.register_decorator = create_registry_decorator(self.registry)

    def test_decorator_registration(self):
        """Test decorator registers prompts correctly."""

        @self.register_decorator(
            name="test_prompt",
            description="Test prompt",
            category="test",
            tags=["test"],
        )
        def create_test_prompt():
            return Mock(spec=BasePromptTemplate)

        # Call the function to trigger registration
        create_test_prompt()

        assert self.registry.has_item("test_prompt")

        metadata = self.registry.get_metadata("test_prompt")
        assert metadata.name == "test_prompt"
        assert metadata.description == "Test prompt"
        assert metadata.category == "test"
        assert metadata.tags == ["test"]

    def test_decorator_with_minimal_args(self):
        """Test decorator with minimal arguments."""

        @self.register_decorator(name="minimal_prompt")
        def create_minimal_prompt():
            return Mock(spec=BasePromptTemplate)

        # Call the function to trigger registration
        create_minimal_prompt()

        assert self.registry.has_item("minimal_prompt")

        metadata = self.registry.get_metadata("minimal_prompt")
        assert metadata.name == "minimal_prompt"
        assert metadata.description == ""
        assert metadata.category == "general"


class TestGlobalRegistry:
    """Test the global registry instance."""

    def test_global_registry_exists(self):
        """Test that global registry exists and is accessible."""
        assert isinstance(prompt_registry, PromptRegistry)

    def test_convenience_functions(self):
        """Test convenience functions work with global registry."""
        mock_template = Mock(spec=BasePromptTemplate)

        # Register using global registry directly
        prompt_registry.register("global_test", mock_template)

        # Test convenience functions
        assert get_prompt("global_test") == mock_template
        assert "global_test" in list_available_prompts()
        assert "global_test" in search_prompts("global")

        # Cleanup
        prompt_registry.unregister("global_test")

    def test_convenience_function_list_with_category(self):
        """Test list_available_prompts with category filter."""
        mock_template = Mock(spec=BasePromptTemplate)

        prompt_registry.register("cat_test", mock_template, category="test_cat")

        # Test category filtering
        all_prompts = list_available_prompts()
        cat_prompts = list_available_prompts(category="test_cat")

        assert "cat_test" in all_prompts
        assert "cat_test" in cat_prompts

        # Cleanup
        prompt_registry.unregister("cat_test")

    def test_convenience_function_search_with_categories(self):
        """Test search_prompts with categories filter."""
        mock_template1 = Mock(spec=BasePromptTemplate)
        mock_template2 = Mock(spec=BasePromptTemplate)

        prompt_registry.register("search_test1", mock_template1, category="cat1")
        prompt_registry.register("search_test2", mock_template2, category="cat2")

        # Test category filtering in search
        results = search_prompts("search", categories=["cat1"])
        assert "search_test1" in results
        assert "search_test2" not in results

        # Cleanup
        prompt_registry.unregister("search_test1")
        prompt_registry.unregister("search_test2")


class TestRegistryIntegration:
    """Test registry integration with actual prompt templates."""

    def setup_method(self):
        """Setup for each test method."""
        self.registry = PromptRegistry()

    def test_register_chat_prompt_template(self):
        """Test registering ChatPromptTemplate."""
        template = ChatPromptTemplate.from_messages(
            [("system", "You are a helpful assistant."), ("user", "{input}")]
        )

        self.registry.register("chat_prompt", template)

        retrieved = self.registry.get("chat_prompt")
        assert isinstance(retrieved, ChatPromptTemplate)
        assert retrieved.input_variables == ["input"]

    def test_register_prompt_template(self):
        """Test registering basic PromptTemplate."""
        template = PromptTemplate.from_template("Answer the question: {question}")

        self.registry.register("simple_prompt", template)

        retrieved = self.registry.get("simple_prompt")
        assert isinstance(retrieved, PromptTemplate)
        assert retrieved.input_variables == ["question"]

    def test_prompt_formatting_after_registry(self):
        """Test that prompts work correctly after registry retrieval."""
        template = PromptTemplate.from_template("Hello {name}!")

        self.registry.register("greeting", template)

        retrieved = self.registry.get("greeting")
        formatted = retrieved.format(name="World")
        assert formatted == "Hello World!"

    def test_chat_prompt_formatting_after_registry(self):
        """Test chat prompts work correctly after registry retrieval."""
        template = ChatPromptTemplate.from_messages(
            [("system", "You are {role}."), ("user", "{message}")]
        )

        self.registry.register("chat_greeting", template)

        retrieved = self.registry.get("chat_greeting")
        formatted = retrieved.format(role="assistant", message="Hello!")
        assert "assistant" in formatted
        assert "Hello!" in formatted
