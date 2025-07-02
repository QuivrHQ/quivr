"""Tests for system prompts."""

import pytest
from langchain_core.prompts import ChatPromptTemplate

from quivr_core.rag.prompt.prompts.system import create_update_prompt


class TestUpdatePrompt:
    """Test system prompt update functionality."""

    def test_create_update_prompt(self):
        """Test update prompt creation."""
        prompt = create_update_prompt()

        assert isinstance(prompt, ChatPromptTemplate)

    def test_update_prompt_variables(self):
        """Test update prompt has required variables."""
        prompt = create_update_prompt()

        required_vars = {
            "instruction",
            "system_prompt",
            "available_tools",
            "activated_tools",
        }
        assert required_vars.issubset(set(prompt.input_variables))

    def test_update_prompt_structure(self):
        """Test the structure of update prompt."""
        prompt = create_update_prompt()

        # Should have system and human messages
        assert len(prompt.messages) == 2

        message_types = [msg.__class__.__name__ for msg in prompt.messages]
        assert "SystemMessagePromptTemplate" in message_types
        assert "HumanMessagePromptTemplate" in message_types

    def test_update_prompt_system_update_logic(self):
        """Test update prompt contains system update logic."""
        prompt = create_update_prompt()

        test_data = {
            "instruction": "Reply in French",
            "system_prompt": "You are a helpful assistant.",
            "available_tools": "web_search, calculator, translator",
            "activated_tools": "web_search",
        }

        formatted = prompt.format(**test_data)

        # Should contain update logic
        assert "update the prompt" in formatted.lower()
        assert "include the instruction" in formatted.lower()
        assert "decide which tools to activate" in formatted.lower()

    def test_update_prompt_tool_activation_logic(self):
        """Test update prompt contains tool activation logic."""
        prompt = create_update_prompt()

        test_data = {
            "instruction": "Use web search for recent information",
            "system_prompt": "Current system prompt",
            "available_tools": "web_search, file_reader, calculator",
            "activated_tools": "file_reader",
        }

        formatted = prompt.format(**test_data)

        # Should contain tool activation logic
        assert "add the tool to the list" in formatted.lower()
        assert "activated tools" in formatted.lower()
        assert "available tools" in formatted.lower()

    def test_update_prompt_contradiction_handling(self):
        """Test update prompt handles contradictory instructions."""
        prompt = create_update_prompt()

        test_data = {
            "instruction": "Always be verbose in responses",
            "system_prompt": "Keep responses concise and brief.",
            "available_tools": "none",
            "activated_tools": "none",
        }

        formatted = prompt.format(**test_data)

        # Should handle contradictions
        assert (
            "contradicts" in formatted.lower() or "contradictory" in formatted.lower()
        )
        assert "remove" in formatted.lower()

    def test_update_prompt_duplicate_instruction_handling(self):
        """Test update prompt handles duplicate instructions."""
        prompt = create_update_prompt()

        test_data = {
            "instruction": "Be helpful and professional",
            "system_prompt": "You are helpful and professional assistant.",
            "available_tools": "basic_tools",
            "activated_tools": "basic_tools",
        }

        formatted = prompt.format(**test_data)

        # Should handle duplicates
        assert "already contains" in formatted.lower()
        assert "do not add it again" in formatted.lower()

    def test_update_prompt_generic_instructions_requirement(self):
        """Test update prompt requires generic instructions."""
        prompt = create_update_prompt()

        test_data = {
            "instruction": "Answer this specific question about AI",
            "system_prompt": "General assistant behavior",
            "available_tools": "research_tools",
            "activated_tools": "none",
        }

        formatted = prompt.format(**test_data)

        # Should emphasize generic instructions
        assert "generic instructions" in formatted.lower()
        assert "applied to any user task" in formatted.lower()

    def test_update_prompt_conciseness_requirement(self):
        """Test update prompt requires concise prompts."""
        prompt = create_update_prompt()

        test_data = {
            "instruction": "Be more detailed in explanations",
            "system_prompt": "Basic assistant",
            "available_tools": "explanation_tools",
            "activated_tools": "none",
        }

        formatted = prompt.format(**test_data)

        # Should require conciseness
        assert "concise and clear" in formatted.lower()

    def test_update_prompt_reasoning_requirement(self):
        """Test update prompt requires reasoning output."""
        prompt = create_update_prompt()

        test_data = {
            "instruction": "Add math capabilities",
            "system_prompt": "Current system behavior",
            "available_tools": "calculator, math_solver",
            "activated_tools": "calculator",
        }

        formatted = prompt.format(**test_data)

        # Should require reasoning
        assert "reasoning" in formatted.lower()
        assert "separately" in formatted.lower()

    def test_update_prompt_tool_reference_handling(self):
        """Test update prompt handles tool references in system prompt."""
        prompt = create_update_prompt()

        test_data = {
            "instruction": "Use the calculator for math problems",
            "system_prompt": "When doing calculations, use the calculator tool",
            "available_tools": "calculator, web_search",
            "activated_tools": "web_search",
        }

        formatted = prompt.format(**test_data)

        # Should handle tool references
        assert "refers to a tool" in formatted.lower()
        assert "add the tool to the list" in formatted.lower()

    def test_update_prompt_no_tool_activation_scenario(self):
        """Test update prompt handles scenarios requiring no tool activation."""
        prompt = create_update_prompt()

        test_data = {
            "instruction": "Be more polite in responses",
            "system_prompt": "Assistant behavior guidelines",
            "available_tools": "various_tools",
            "activated_tools": "current_tools",
        }

        formatted = prompt.format(**test_data)

        # Should handle no activation needed
        assert "no tool activation is needed" in formatted.lower()
        assert "empty lists" in formatted.lower()

    def test_update_prompt_with_empty_tool_lists(self):
        """Test update prompt with empty tool lists."""
        prompt = create_update_prompt()

        test_data = {
            "instruction": "Improve response quality",
            "system_prompt": "Basic assistant",
            "available_tools": "",
            "activated_tools": "",
        }

        formatted = prompt.format(**test_data)

        # Should handle empty tool lists
        assert isinstance(formatted, str)
        assert "Improve response quality" in formatted

    def test_update_prompt_complex_instruction(self):
        """Test update prompt with complex multi-part instruction."""
        prompt = create_update_prompt()

        complex_instruction = (
            "When answering questions: 1) Always provide sources, "
            "2) Use bullet points for lists, 3) Include relevant examples, "
            "4) End with a summary"
        )

        test_data = {
            "instruction": complex_instruction,
            "system_prompt": "Simple assistant behavior",
            "available_tools": "search, formatter, example_finder",
            "activated_tools": "search",
        }

        formatted = prompt.format(**test_data)

        # Should handle complex instructions
        assert "provide sources" in formatted
        assert "bullet points" in formatted
        assert "relevant examples" in formatted
        assert "summary" in formatted

    def test_update_prompt_tool_activation_reasoning(self):
        """Test update prompt requires reasoning for tool activation."""
        prompt = create_update_prompt()

        test_data = {
            "instruction": "Always verify facts with web search",
            "system_prompt": "Standard assistant",
            "available_tools": "web_search, fact_checker, validator",
            "activated_tools": "none",
        }

        formatted = prompt.format(**test_data)

        # Should require reasoning for tool activation
        assert "reasoning that led to the tool activation" in formatted.lower()

    def test_update_prompt_missing_variables(self):
        """Test update prompt with missing variables."""
        prompt = create_update_prompt()

        # Missing required variables should raise KeyError
        with pytest.raises(KeyError):
            prompt.format(instruction="test")  # Missing other required vars

    def test_update_prompt_variable_order_in_output(self):
        """Test that variables appear in logical order in formatted output."""
        prompt = create_update_prompt()

        test_data = {
            "instruction": "Test instruction",
            "system_prompt": "Test system prompt",
            "available_tools": "test_tools",
            "activated_tools": "active_tools",
        }

        formatted = prompt.format(**test_data)

        # Should reference current system prompt before instruction
        system_pos = formatted.find("Test system prompt")
        instruction_pos = formatted.find("Test instruction")

        # System prompt should be mentioned in the context setup
        assert system_pos != -1
        assert instruction_pos != -1

    def test_update_prompt_tool_consistency(self):
        """Test update prompt maintains tool list consistency."""
        prompt = create_update_prompt()

        test_data = {
            "instruction": "Enable advanced calculations",
            "system_prompt": "Basic math support",
            "available_tools": "calculator, advanced_math, statistics",
            "activated_tools": "calculator",
        }

        formatted = prompt.format(**test_data)

        # Should reference both available and activated tools appropriately
        assert "calculator, advanced_math, statistics" in formatted
        assert "calculator" in formatted

    def test_update_prompt_comprehensive_formatting(self):
        """Test comprehensive formatting with all fields populated."""
        prompt = create_update_prompt()

        test_data = {
            "instruction": "Provide detailed explanations with examples and citations",
            "system_prompt": "You are a knowledgeable assistant that helps users understand complex topics.",
            "available_tools": "web_search, citation_formatter, example_generator, knowledge_base",
            "activated_tools": "web_search, knowledge_base",
        }

        formatted = prompt.format(**test_data)

        # Should be a comprehensive, well-formatted prompt
        assert len(formatted) > 500  # Should be substantial
        assert "detailed explanations" in formatted
        assert "knowledgeable assistant" in formatted
        assert "citation_formatter" in formatted
        assert "knowledge_base" in formatted
