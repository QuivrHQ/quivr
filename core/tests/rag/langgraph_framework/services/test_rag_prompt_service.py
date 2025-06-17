"""Tests for the RAG Prompt service."""

import pytest
from unittest.mock import patch, Mock
from langchain_core.prompts.base import BasePromptTemplate

from quivr_core.rag.langgraph_framework.services.rag_prompt_service import (
    RAGPromptService,
)
from quivr_core.rag.prompts import TemplatePromptName


class TestRAGPromptServiceInitialization:
    """Test RAG Prompt service initialization."""

    def test_initialization(self):
        """Test RAG prompt service initialization."""
        with patch(
            "quivr_core.rag.langgraph_framework.services.rag_prompt_service.custom_prompts"
        ):
            service = RAGPromptService()

            # Should initialize without errors
            assert isinstance(service, RAGPromptService)
            assert hasattr(service, "templates")


class TestRAGPromptServiceTemplateRetrieval:
    """Test template retrieval functionality."""

    @pytest.fixture(scope="function")
    def prompt_service(self):
        """Create a RAG prompt service instance."""
        with patch(
            "quivr_core.rag.langgraph_framework.services.rag_prompt_service.custom_prompts"
        ) as mock_prompts:
            service = RAGPromptService()
            return service, mock_prompts

    def test_get_template_rag_answer(self, prompt_service):
        """Test getting RAG answer template."""
        service, mock_prompts = prompt_service

        # Create a mock template
        mock_template = Mock(spec=BasePromptTemplate)
        mock_prompts.__getitem__.return_value = mock_template

        result = service.get_template(TemplatePromptName.RAG_ANSWER_PROMPT)

        assert result == mock_template
        mock_prompts.__getitem__.assert_called_once_with(
            TemplatePromptName.RAG_ANSWER_PROMPT
        )

    def test_get_template_different_types(self, prompt_service):
        """Test getting different template types."""
        service, mock_prompts = prompt_service

        # Test different template names
        template_names = [
            TemplatePromptName.RAG_ANSWER_PROMPT,
            # Add other template names as they become available
        ]

        for template_name in template_names:
            mock_template = Mock(spec=BasePromptTemplate)
            mock_prompts.__getitem__.return_value = mock_template

            result = service.get_template(template_name)

            assert result == mock_template

    def test_get_template_with_invalid_name(self, prompt_service):
        """Test getting template with invalid name."""
        service, mock_prompts = prompt_service

        mock_prompts.__getitem__.side_effect = KeyError("Invalid template name")

        with pytest.raises(KeyError):
            service.get_template("invalid_template_name")

    def test_templates_property_access(self, prompt_service):
        """Test that templates property is accessible."""
        service, mock_prompts = prompt_service

        # Should be able to access the templates property
        assert service.templates == mock_prompts


class TestRAGPromptServiceIntegration:
    """Test integration aspects of the prompt service."""

    def test_service_can_be_used_in_dependency_injection(self):
        """Test that the service can be used in dependency injection context."""
        with patch(
            "quivr_core.rag.langgraph_framework.services.rag_prompt_service.custom_prompts"
        ):
            service = RAGPromptService()

            # Should have the expected method
            assert hasattr(service, "get_template")
            assert callable(getattr(service, "get_template"))

    def test_service_stateless_behavior(self):
        """Test that the service behaves in a stateless manner."""
        with patch(
            "quivr_core.rag.langgraph_framework.services.rag_prompt_service.custom_prompts"
        ) as mock_prompts:
            mock_template = Mock(spec=BasePromptTemplate)
            mock_prompts.__getitem__.return_value = mock_template

            service1 = RAGPromptService()
            service2 = RAGPromptService()

            result1 = service1.get_template(TemplatePromptName.RAG_ANSWER_PROMPT)
            result2 = service2.get_template(TemplatePromptName.RAG_ANSWER_PROMPT)

            assert result1 == result2 == mock_template

    def test_service_initialization_with_custom_prompts(self):
        """Test that service properly initializes with custom prompts."""
        mock_custom_prompts = {"test_template": Mock(spec=BasePromptTemplate)}

        with patch(
            "quivr_core.rag.langgraph_framework.services.rag_prompt_service.custom_prompts",
            mock_custom_prompts,
        ):
            service = RAGPromptService()

            assert service.templates == mock_custom_prompts
