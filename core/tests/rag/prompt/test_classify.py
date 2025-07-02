"""Tests for classification prompts."""

import pytest
from langchain_core.prompts import ChatPromptTemplate

from quivr_core.rag.prompt.prompts.classify import (
    create_user_intent_prompt,
    create_tool_routing_prompt,
)


class TestUserIntentPrompt:
    """Test user intent classification prompt."""

    def test_create_user_intent_prompt(self):
        """Test user intent prompt creation."""
        prompt = create_user_intent_prompt()

        assert isinstance(prompt, ChatPromptTemplate)
        assert "task" in prompt.input_variables

    def test_user_intent_prompt_structure(self):
        """Test the structure of user intent prompt."""
        prompt = create_user_intent_prompt()

        # Should have system and human messages
        assert len(prompt.messages) == 2

        # Check message types
        message_types = [msg.__class__.__name__ for msg in prompt.messages]
        assert "SystemMessagePromptTemplate" in message_types
        assert "HumanMessagePromptTemplate" in message_types

    def test_user_intent_prompt_content(self):
        """Test user intent prompt contains expected content."""
        prompt = create_user_intent_prompt()

        # Format to get the actual content
        formatted = prompt.format(task="Can you reply in French?")

        # Should contain key instructions
        assert "user intent" in formatted.lower()
        assert "instructions" in formatted.lower()
        assert "task" in formatted.lower()
        assert "prompt" in formatted.lower()

    def test_user_intent_prompt_examples(self):
        """Test user intent prompt contains example scenarios."""
        prompt = create_user_intent_prompt()
        formatted = prompt.format(task="test")

        # Should contain example instructions
        assert "reply in French" in formatted or "Answer in French" in formatted
        assert "expert legal assistant" in formatted
        assert "behave as" in formatted

    def test_user_intent_prompt_formatting_with_instruction(self):
        """Test formatting with instruction-type input."""
        prompt = create_user_intent_prompt()

        instruction_task = "Can you reply in Spanish from now on?"
        formatted = prompt.format(task=instruction_task)

        assert instruction_task in formatted
        assert isinstance(formatted, str)

    def test_user_intent_prompt_formatting_with_task(self):
        """Test formatting with task-type input."""
        prompt = create_user_intent_prompt()

        task_input = "What is the capital of France?"
        formatted = prompt.format(task=task_input)

        assert task_input in formatted
        assert isinstance(formatted, str)

    def test_user_intent_prompt_required_variables(self):
        """Test that required variables are properly defined."""
        prompt = create_user_intent_prompt()

        # Should only require 'task' variable
        assert prompt.input_variables == ["task"]

    def test_user_intent_prompt_missing_variable_raises_error(self):
        """Test that missing required variables raise KeyError."""
        prompt = create_user_intent_prompt()

        with pytest.raises(KeyError):
            prompt.format()  # Missing 'task' variable


class TestToolRoutingPrompt:
    """Test tool routing prompt."""

    def test_create_tool_routing_prompt(self):
        """Test tool routing prompt creation."""
        prompt = create_tool_routing_prompt()

        assert isinstance(prompt, ChatPromptTemplate)

    def test_tool_routing_prompt_variables(self):
        """Test tool routing prompt has required variables."""
        prompt = create_tool_routing_prompt()

        required_vars = {"context", "activated_tools", "tasks", "chat_history"}
        assert required_vars.issubset(set(prompt.input_variables))

    def test_tool_routing_prompt_structure(self):
        """Test the structure of tool routing prompt."""
        prompt = create_tool_routing_prompt()

        # Should have system, chat history placeholder, system, and human messages
        assert len(prompt.messages) == 4

        message_types = [msg.__class__.__name__ for msg in prompt.messages]
        assert "SystemMessagePromptTemplate" in message_types
        assert "MessagesPlaceholder" in message_types
        assert "HumanMessagePromptTemplate" in message_types

    def test_tool_routing_prompt_content(self):
        """Test tool routing prompt contains expected content."""
        prompt = create_tool_routing_prompt()

        test_data = {
            "context": "Sample context about the topic",
            "activated_tools": "web_search, calculator",
            "tasks": "What is 2+2? Search for recent news.",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should contain key routing concepts
        assert "tasks" in formatted.lower()
        assert "context" in formatted.lower()
        assert "tools" in formatted.lower()
        assert "completed fully" in formatted.lower()

    def test_tool_routing_prompt_decision_logic(self):
        """Test tool routing prompt contains decision logic."""
        prompt = create_tool_routing_prompt()

        test_data = {
            "context": "Limited context",
            "activated_tools": "search_tool",
            "tasks": "Find information about AI",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should contain decision-making instructions
        assert "determine whether" in formatted.lower()
        assert "necessary to complete" in formatted.lower()
        assert "most appropriate" in formatted.lower()

    def test_tool_routing_prompt_tool_selection_guidance(self):
        """Test tool routing prompt provides tool selection guidance."""
        prompt = create_tool_routing_prompt()

        test_data = {
            "context": "Context without complete information",
            "activated_tools": "tool1, tool2, tool3",
            "tasks": "Complex task requiring external data",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should contain tool selection guidance
        assert "select the tool most appropriate" in formatted.lower()
        assert "only the list of tools below" in formatted.lower()
        assert "not listed among the available tools" in formatted.lower()

    def test_tool_routing_prompt_no_tools_handling(self):
        """Test tool routing prompt handles no tools scenario."""
        prompt = create_tool_routing_prompt()

        test_data = {
            "context": "Complete context with all information",
            "activated_tools": "",
            "tasks": "Simple task that can be completed with context",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should handle no tools scenario
        assert "no tools are listed" in formatted.lower()
        assert "return the tasks as is" in formatted.lower()

    def test_tool_routing_prompt_with_chat_history(self):
        """Test tool routing prompt with chat history."""
        prompt = create_tool_routing_prompt()

        test_data = {
            "context": "Current context",
            "activated_tools": "search_tool",
            "tasks": "Follow up on previous discussion",
            "chat_history": [
                {"role": "user", "content": "Tell me about AI"},
                {"role": "assistant", "content": "AI is artificial intelligence..."},
            ],
        }

        formatted = prompt.format(**test_data)

        # Should work with chat history
        assert isinstance(formatted, str)
        assert "Follow up on previous discussion" in formatted

    def test_tool_routing_prompt_context_sufficiency(self):
        """Test tool routing prompt evaluates context sufficiency."""
        prompt = create_tool_routing_prompt()

        test_data = {
            "context": "Comprehensive context with all needed information",
            "activated_tools": "web_search, calculator",
            "tasks": "Summarize the provided information",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should evaluate context sufficiency
        assert "contain all the information necessary" in formatted.lower()
        assert "chat history" in formatted.lower()

    def test_tool_routing_prompt_formatting_edge_cases(self):
        """Test tool routing prompt handles edge cases."""
        prompt = create_tool_routing_prompt()

        # Test with empty strings
        test_data = {
            "context": "",
            "activated_tools": "",
            "tasks": "",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)
        assert isinstance(formatted, str)

        # Test with None values converted to strings
        test_data_none = {
            "context": "None",
            "activated_tools": "None",
            "tasks": "None",
            "chat_history": [],
        }

        formatted_none = prompt.format(**test_data_none)
        assert isinstance(formatted_none, str)

    def test_tool_routing_prompt_missing_variables(self):
        """Test tool routing prompt with missing variables."""
        prompt = create_tool_routing_prompt()

        # Missing required variables should raise KeyError
        with pytest.raises(KeyError):
            prompt.format(context="test")  # Missing other required vars

    def test_tool_routing_prompt_task_separation(self):
        """Test tool routing prompt handles task separation."""
        prompt = create_tool_routing_prompt()

        test_data = {
            "context": "Limited context",
            "activated_tools": "tool1, tool2",
            "tasks": "Task 1: Do this. Task 2: Do that.",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should handle multiple tasks
        assert "consider each task separately" in formatted.lower()
        assert "Task 1" in formatted
        assert "Task 2" in formatted


class TestClassifyPromptsIntegration:
    """Test integration between classification prompts."""

    def test_both_prompts_are_chat_templates(self):
        """Test both classification prompts are ChatPromptTemplates."""
        user_intent = create_user_intent_prompt()
        tool_routing = create_tool_routing_prompt()

        assert isinstance(user_intent, ChatPromptTemplate)
        assert isinstance(tool_routing, ChatPromptTemplate)

    def test_prompts_have_different_purposes(self):
        """Test prompts serve different classification purposes."""
        user_intent = create_user_intent_prompt()
        tool_routing = create_tool_routing_prompt()

        # User intent should be simpler (fewer variables)
        assert len(user_intent.input_variables) < len(tool_routing.input_variables)

        # Tool routing should handle more complex scenarios
        assert "chat_history" in tool_routing.input_variables
        assert "chat_history" not in user_intent.input_variables

    def test_prompts_complement_each_other(self):
        """Test that prompts can work together in a pipeline."""
        user_intent = create_user_intent_prompt()
        tool_routing = create_tool_routing_prompt()

        # User intent determines if input is instruction or task
        intent_result = user_intent.format(task="What is machine learning?")
        assert isinstance(intent_result, str)

        # Tool routing then determines how to handle the task
        routing_result = tool_routing.format(
            context="Basic ML information available",
            activated_tools="web_search",
            tasks="What is machine learning?",
            chat_history=[],
        )
        assert isinstance(routing_result, str)

        # Both should process the same task differently
        assert "machine learning" in intent_result.lower()
        assert "machine learning" in routing_result.lower()
