from unittest.mock import patch

import pytest
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.prompts.base import BasePromptTemplate

from quivr_core.rag.prompts import (
    TemplatePromptName,
    custom_prompts,
    _define_custom_prompts,
)


class TestTemplatePromptName:
    """Test the TemplatePromptName enum."""

    def test_all_prompt_names_exist(self):
        """Test that all expected prompt names are defined."""
        expected_prompts = [
            "ZENDESK_TEMPLATE_PROMPT",
            "TOOL_ROUTING_PROMPT",
            "RAG_ANSWER_PROMPT",
            "CONDENSE_TASK_PROMPT",
            "DEFAULT_DOCUMENT_PROMPT",
            "CHAT_LLM_PROMPT",
            "USER_INTENT_PROMPT",
            "UPDATE_PROMPT",
            "SPLIT_PROMPT",
            "ZENDESK_LLM_PROMPT",
        ]

        for prompt_name in expected_prompts:
            assert hasattr(TemplatePromptName, prompt_name)
            assert getattr(TemplatePromptName, prompt_name) == prompt_name

    def test_prompt_name_values(self):
        """Test that prompt names have correct string values."""
        assert TemplatePromptName.RAG_ANSWER_PROMPT == "RAG_ANSWER_PROMPT"
        assert TemplatePromptName.CONDENSE_TASK_PROMPT == "CONDENSE_TASK_PROMPT"
        assert TemplatePromptName.DEFAULT_DOCUMENT_PROMPT == "DEFAULT_DOCUMENT_PROMPT"


class TestCustomPrompts:
    """Test the custom prompts dictionary and templates."""

    def test_all_prompts_defined(self):
        """Test that all prompt names have corresponding prompts."""
        for prompt_name in TemplatePromptName:
            assert prompt_name in custom_prompts
            assert isinstance(custom_prompts[prompt_name], BasePromptTemplate)

    def test_custom_prompts_immutable(self):
        """Test that custom_prompts is immutable."""
        with pytest.raises(TypeError):
            custom_prompts[TemplatePromptName.RAG_ANSWER_PROMPT] = (
                PromptTemplate.from_template("test")
            )

    def test_rag_answer_prompt_structure(self):
        """Test the RAG answer prompt has correct structure."""
        prompt = custom_prompts[TemplatePromptName.RAG_ANSWER_PROMPT]
        assert isinstance(prompt, ChatPromptTemplate)

        # Check required variables
        expected_vars = {
            "custom_instructions",
            "context",
            "files",
            "chat_history",
            "task",
            "rephrased_task",
        }
        assert expected_vars.issubset(set(prompt.input_variables))

    def test_condense_task_prompt_structure(self):
        """Test the condense task prompt has correct structure."""
        prompt = custom_prompts[TemplatePromptName.CONDENSE_TASK_PROMPT]
        assert isinstance(prompt, ChatPromptTemplate)

        expected_vars = {"task", "chat_history"}
        assert expected_vars.issubset(set(prompt.input_variables))

    def test_default_document_prompt_structure(self):
        """Test the default document prompt has correct structure."""
        prompt = custom_prompts[TemplatePromptName.DEFAULT_DOCUMENT_PROMPT]
        assert isinstance(prompt, PromptTemplate)

        expected_vars = {"original_file_name", "index", "page_content"}
        assert expected_vars.issubset(set(prompt.input_variables))

    def test_chat_llm_prompt_structure(self):
        """Test the chat LLM prompt has correct structure."""
        prompt = custom_prompts[TemplatePromptName.CHAT_LLM_PROMPT]
        assert isinstance(prompt, ChatPromptTemplate)

        expected_vars = {"custom_instructions", "task", "chat_history"}
        assert expected_vars.issubset(set(prompt.input_variables))

    def test_user_intent_prompt_structure(self):
        """Test the user intent prompt has correct structure."""
        prompt = custom_prompts[TemplatePromptName.USER_INTENT_PROMPT]
        assert isinstance(prompt, ChatPromptTemplate)

        expected_vars = {"task"}
        assert expected_vars.issubset(set(prompt.input_variables))

    def test_update_prompt_structure(self):
        """Test the update prompt has correct structure."""
        prompt = custom_prompts[TemplatePromptName.UPDATE_PROMPT]
        assert isinstance(prompt, ChatPromptTemplate)

        expected_vars = {
            "instruction",
            "system_prompt",
            "available_tools",
            "activated_tools",
        }
        assert expected_vars.issubset(set(prompt.input_variables))

    def test_split_prompt_structure(self):
        """Test the split prompt has correct structure."""
        prompt = custom_prompts[TemplatePromptName.SPLIT_PROMPT]
        assert isinstance(prompt, ChatPromptTemplate)

        expected_vars = {"user_input", "chat_history"}
        assert expected_vars.issubset(set(prompt.input_variables))

    def test_tool_routing_prompt_structure(self):
        """Test the tool routing prompt has correct structure."""
        prompt = custom_prompts[TemplatePromptName.TOOL_ROUTING_PROMPT]
        assert isinstance(prompt, ChatPromptTemplate)

        expected_vars = {"context", "activated_tools", "tasks", "chat_history"}
        assert expected_vars.issubset(set(prompt.input_variables))

    def test_zendesk_template_prompt_structure(self):
        """Test the Zendesk template prompt has correct structure."""
        prompt = custom_prompts[TemplatePromptName.ZENDESK_TEMPLATE_PROMPT]
        assert isinstance(prompt, ChatPromptTemplate)

        expected_vars = {
            "current_time",
            "guidelines",
            "user_metadata",
            "ticket_metadata",
            "similar_tickets",
            "ticket_history",
            "additional_information",
            "client_query",
        }
        assert expected_vars.issubset(set(prompt.input_variables))

    def test_zendesk_llm_prompt_structure(self):
        """Test the Zendesk LLM prompt has correct structure."""
        prompt = custom_prompts[TemplatePromptName.ZENDESK_LLM_PROMPT]
        assert isinstance(prompt, ChatPromptTemplate)

        expected_vars = {"enforced_system_prompt", "task", "chat_history"}
        assert expected_vars.issubset(set(prompt.input_variables))


class TestPromptTemplateFormatting:
    """Test that prompts can be formatted with sample data."""

    def test_rag_answer_prompt_formatting(self):
        """Test RAG answer prompt can be formatted."""
        prompt = custom_prompts[TemplatePromptName.RAG_ANSWER_PROMPT]

        test_data = {
            "custom_instructions": "Answer concisely",
            "context": "Sample context",
            "files": "file1.txt, file2.txt",
            "chat_history": [],
            "task": "What is the main topic?",
            "rephrased_task": "What is the main topic discussed?",
        }

        formatted = prompt.format(**test_data)
        assert isinstance(formatted, str)
        assert "Answer concisely" in formatted
        assert "Sample context" in formatted
        assert "What is the main topic?" in formatted

    def test_default_document_prompt_formatting(self):
        """Test default document prompt can be formatted."""
        prompt = custom_prompts[TemplatePromptName.DEFAULT_DOCUMENT_PROMPT]

        test_data = {
            "original_file_name": "test.pdf",
            "index": 1,
            "page_content": "This is sample content",
        }

        formatted = prompt.format(**test_data)
        assert "test.pdf" in formatted
        assert "1" in formatted
        assert "This is sample content" in formatted

    def test_chat_llm_prompt_formatting(self):
        """Test chat LLM prompt can be formatted."""
        prompt = custom_prompts[TemplatePromptName.CHAT_LLM_PROMPT]

        test_data = {
            "custom_instructions": "Be helpful",
            "task": "Explain quantum computing",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)
        assert isinstance(formatted, str)
        assert "Be helpful" in formatted
        assert "Explain quantum computing" in formatted

    def test_condense_task_prompt_formatting(self):
        """Test condense task prompt can be formatted."""
        prompt = custom_prompts[TemplatePromptName.CONDENSE_TASK_PROMPT]

        test_data = {"task": "Tell me more about that", "chat_history": []}

        formatted = prompt.format(**test_data)
        assert isinstance(formatted, str)
        assert "Tell me more about that" in formatted


class TestPromptDateHandling:
    """Test that prompts handle date formatting correctly."""

    @patch("quivr_core.rag.prompts.datetime")
    def test_date_formatting_in_prompts(self, mock_datetime):
        """Test that current date is properly formatted in prompts."""
        # Mock datetime to return a specific date
        mock_datetime.datetime.now.return_value.strftime.return_value = (
            "January 15, 2024"
        )

        # Re-generate prompts with mocked date
        prompts = _define_custom_prompts()

        # Check that date appears in relevant prompts
        rag_prompt = prompts[TemplatePromptName.RAG_ANSWER_PROMPT]
        chat_prompt = prompts[TemplatePromptName.CHAT_LLM_PROMPT]

        # Format with minimal data to check date inclusion
        rag_formatted = rag_prompt.format(
            custom_instructions="",
            context="",
            files="",
            chat_history=[],
            task="",
            rephrased_task="",
        )
        chat_formatted = chat_prompt.format(
            custom_instructions="", task="", chat_history=[]
        )

        assert "January 15, 2024" in rag_formatted
        assert "January 15, 2024" in chat_formatted


class TestPromptContentValidation:
    """Test that prompts contain expected content and instructions."""

    def test_rag_prompt_contains_quivr_name(self):
        """Test that RAG prompt identifies the assistant as Quivr."""
        prompt = custom_prompts[TemplatePromptName.RAG_ANSWER_PROMPT]
        formatted = prompt.format(
            custom_instructions="",
            context="",
            files="",
            chat_history=[],
            task="",
            rephrased_task="",
        )
        assert "Quivr" in formatted

    def test_rag_prompt_contains_markdown_instruction(self):
        """Test that RAG prompt contains markdown formatting instruction."""
        prompt = custom_prompts[TemplatePromptName.RAG_ANSWER_PROMPT]
        formatted = prompt.format(
            custom_instructions="",
            context="",
            files="",
            chat_history=[],
            task="",
            rephrased_task="",
        )
        assert "markdown" in formatted.lower()

    def test_rag_prompt_contains_context_only_instruction(self):
        """Test that RAG prompt instructs to use only provided context."""
        prompt = custom_prompts[TemplatePromptName.RAG_ANSWER_PROMPT]
        formatted = prompt.format(
            custom_instructions="",
            context="",
            files="",
            chat_history=[],
            task="",
            rephrased_task="",
        )
        assert "ONLY the provided context" in formatted

    def test_condense_task_prompt_contains_standalone_instruction(self):
        """Test that condense task prompt instructs to make standalone tasks."""
        prompt = custom_prompts[TemplatePromptName.CONDENSE_TASK_PROMPT]
        formatted = prompt.format(task="", chat_history=[])
        assert "standalone" in formatted.lower()

    def test_user_intent_prompt_contains_intent_classification(self):
        """Test that user intent prompt contains intent classification instructions."""
        prompt = custom_prompts[TemplatePromptName.USER_INTENT_PROMPT]
        formatted = prompt.format(task="")
        assert "instructions" in formatted.lower()
        assert "task" in formatted.lower()

    def test_zendesk_prompts_contain_customer_service_context(self):
        """Test that Zendesk prompts contain customer service context."""
        zendesk_prompt = custom_prompts[TemplatePromptName.ZENDESK_TEMPLATE_PROMPT]
        zendesk_llm_prompt = custom_prompts[TemplatePromptName.ZENDESK_LLM_PROMPT]

        zendesk_formatted = zendesk_prompt.format(
            current_time="",
            guidelines="",
            user_metadata="",
            ticket_metadata="",
            similar_tickets="",
            ticket_history="",
            additional_information="",
            client_query="",
        )
        zendesk_llm_formatted = zendesk_llm_prompt.format(
            enforced_system_prompt="", task="", chat_history=[]
        )

        assert "Customer Service" in zendesk_formatted or "Zendesk" in zendesk_formatted
        assert "customer" in zendesk_llm_formatted.lower()


class TestPromptErrorHandling:
    """Test error handling in prompt formatting."""

    def test_missing_required_variables_raises_error(self):
        """Test that missing required variables raise appropriate errors."""
        prompt = custom_prompts[TemplatePromptName.RAG_ANSWER_PROMPT]

        with pytest.raises(KeyError):
            prompt.format(context="test")  # Missing other required variables

    def test_extra_variables_ignored(self):
        """Test that extra variables are ignored during formatting."""
        prompt = custom_prompts[TemplatePromptName.DEFAULT_DOCUMENT_PROMPT]

        # Should not raise error with extra variables
        formatted = prompt.format(
            original_file_name="test.pdf",
            index=1,
            page_content="content",
            extra_var="ignored",
        )
        assert isinstance(formatted, str)


class TestPromptRegistryConsistency:
    """Test consistency between prompt registry and enum."""

    def test_all_enum_values_in_registry(self):
        """Test that all enum values are present in the prompt registry."""
        for prompt_name in TemplatePromptName:
            assert prompt_name in custom_prompts

    def test_registry_contains_only_enum_values(self):
        """Test that registry doesn't contain extra prompts not in enum."""
        enum_values = set(TemplatePromptName)
        registry_keys = set(custom_prompts.keys())
        assert registry_keys == enum_values

    def test_prompt_types_are_consistent(self):
        """Test that all prompts are proper BasePromptTemplate instances."""
        for prompt_name, prompt in custom_prompts.items():
            assert isinstance(prompt, BasePromptTemplate)
            assert hasattr(prompt, "format")
            assert hasattr(prompt, "input_variables")
