"""Tests for transform prompts."""

from langchain_core.prompts import ChatPromptTemplate

from quivr_core.rag.prompt.prompts.transform import (
    create_condense_task_prompt,
    create_split_prompt,
    create_split_zendesk_ticket_prompt,
)


class TestCondenseTaskPrompt:
    """Test task condensation prompt."""

    def test_create_condense_task_prompt(self):
        """Test condense task prompt creation."""
        prompt = create_condense_task_prompt()

        assert isinstance(prompt, ChatPromptTemplate)

    def test_condense_task_prompt_variables(self):
        """Test condense task prompt has required variables."""
        prompt = create_condense_task_prompt()

        required_vars = {"task", "chat_history"}
        assert required_vars.issubset(set(prompt.input_variables))

    def test_condense_task_prompt_structure(self):
        """Test the structure of condense task prompt."""
        prompt = create_condense_task_prompt()

        # Should have system, chat history, and human messages
        assert len(prompt.messages) == 3

        message_types = [msg.__class__.__name__ for msg in prompt.messages]
        assert "SystemMessagePromptTemplate" in message_types
        assert "MessagesPlaceholder" in message_types
        assert "HumanMessagePromptTemplate" in message_types

    def test_condense_task_prompt_standalone_instruction(self):
        """Test condense task prompt creates standalone tasks."""
        prompt = create_condense_task_prompt()

        test_data = {
            "task": "Tell me more about that topic we discussed",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should emphasize standalone nature
        assert "standalone" in formatted.lower()
        assert "without the chat history" in formatted.lower()

    def test_condense_task_prompt_no_completion_instruction(self):
        """Test condense task prompt doesn't complete tasks."""
        prompt = create_condense_task_prompt()

        test_data = {"task": "What is the capital of France?", "chat_history": []}

        formatted = prompt.format(**test_data)

        # Should not complete the task
        assert (
            "do not complete" in formatted.lower()
            or "not complete" in formatted.lower()
        )
        assert "reformulate" in formatted.lower()

    def test_condense_task_prompt_with_context_reference(self):
        """Test condense task prompt with context-dependent task."""
        prompt = create_condense_task_prompt()

        test_data = {
            "task": "Can you expand on the previous explanation?",
            "chat_history": [
                {"role": "user", "content": "Explain photosynthesis"},
                {"role": "assistant", "content": "Photosynthesis is the process..."},
            ],
        }

        formatted = prompt.format(**test_data)

        # Should handle context references
        assert "expand on the previous explanation" in formatted
        assert "formulate a standalone task" in formatted.lower()

    def test_condense_task_prompt_with_direct_task(self):
        """Test condense task prompt with already standalone task."""
        prompt = create_condense_task_prompt()

        test_data = {
            "task": "What is machine learning?",
            "chat_history": [
                {"role": "user", "content": "Tell me about AI"},
                {"role": "assistant", "content": "AI is..."},
            ],
        }

        formatted = prompt.format(**test_data)

        # Should return task as is if already standalone
        assert "return it as is" in formatted.lower()
        assert "What is machine learning?" in formatted

    def test_condense_task_prompt_reasoning_suppression(self):
        """Test condense task prompt suppresses reasoning output."""
        prompt = create_condense_task_prompt()

        test_data = {"task": "Summarize that document", "chat_history": []}

        formatted = prompt.format(**test_data)

        # Should suppress reasoning
        assert "do not output your reasoning" in formatted.lower()
        assert "just the task" in formatted.lower()


class TestSplitPrompt:
    """Test input splitting prompt."""

    def test_create_split_prompt(self):
        """Test split prompt creation."""
        prompt = create_split_prompt()

        assert isinstance(prompt, ChatPromptTemplate)

    def test_split_prompt_variables(self):
        """Test split prompt has required variables."""
        prompt = create_split_prompt()

        required_vars = {"user_input", "chat_history"}
        assert required_vars.issubset(set(prompt.input_variables))

    def test_split_prompt_structure(self):
        """Test the structure of split prompt."""
        prompt = create_split_prompt()

        # Should have system, chat history, and human messages
        assert len(prompt.messages) == 3

        message_types = [msg.__class__.__name__ for msg in prompt.messages]
        assert "SystemMessagePromptTemplate" in message_types
        assert "MessagesPlaceholder" in message_types
        assert "HumanMessagePromptTemplate" in message_types

    def test_split_prompt_instruction_identification(self):
        """Test split prompt identifies instructions."""
        prompt = create_split_prompt()

        test_data = {
            "user_input": "Can you reply in French from now on? What is the weather today?",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should identify instructions
        assert "instructions" in formatted.lower()
        assert "behave in a certain way" in formatted.lower()
        assert "reply in french" in formatted.lower()

    def test_split_prompt_task_identification(self):
        """Test split prompt identifies tasks."""
        prompt = create_split_prompt()

        test_data = {
            "user_input": "What is AI? How does it work? Explain machine learning.",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should identify tasks
        assert "tasks" in formatted.lower()
        assert "questions" in formatted.lower()
        assert (
            "summarisation" in formatted.lower() or "summarization" in formatted.lower()
        )

    def test_split_prompt_example_handling(self):
        """Test split prompt with example splitting scenario."""
        prompt = create_split_prompt()

        test_data = {
            "user_input": "What is Apple? Who is its CEO? When was it founded?",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should reference the example
        assert "what is apple" in formatted.lower()
        assert (
            "who is its ceo" in formatted.lower()
            or "who is the ceo" in formatted.lower()
        )
        assert (
            "when was it founded" in formatted.lower()
            or "when was apple founded" in formatted.lower()
        )

    def test_split_prompt_standalone_requirement(self):
        """Test split prompt requires standalone tasks."""
        prompt = create_split_prompt()

        test_data = {
            "user_input": "Tell me more about that. Also, what are the benefits?",
            "chat_history": [
                {"role": "user", "content": "Explain renewable energy"},
                {"role": "assistant", "content": "Renewable energy sources..."},
            ],
        }

        formatted = prompt.format(**test_data)

        # Should require standalone tasks
        assert "standalone" in formatted.lower()
        assert "self-contained" in formatted.lower()
        assert "without the chat history" in formatted.lower()

    def test_split_prompt_instruction_condensation(self):
        """Test split prompt condenses instructions."""
        prompt = create_split_prompt()

        test_data = {
            "user_input": "Please be formal. Use proper grammar. Be professional in your responses.",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should condense instructions
        assert "collect and condense" in formatted.lower()
        assert "single string" in formatted.lower()

    def test_split_prompt_no_task_generation(self):
        """Test split prompt doesn't generate new tasks."""
        prompt = create_split_prompt()

        test_data = {"user_input": "Hello there!", "chat_history": []}

        formatted = prompt.format(**test_data)

        # Should not generate new tasks
        assert "not suggest or generate new tasks" in formatted.lower()
        assert "do not try to solve" in formatted.lower()

    def test_split_prompt_fallback_behavior(self):
        """Test split prompt fallback when no tasks found."""
        prompt = create_split_prompt()

        test_data = {"user_input": "Thanks for your help!", "chat_history": []}

        formatted = prompt.format(**test_data)

        # Should have fallback behavior
        assert "no tasks are found" in formatted.lower()
        assert "return the user input as is" in formatted.lower()


class TestSplitZendeskTicketPrompt:
    """Test Zendesk ticket splitting prompt."""

    def test_create_split_zendesk_ticket_prompt(self):
        """Test split Zendesk ticket prompt creation."""
        prompt = create_split_zendesk_ticket_prompt()

        assert isinstance(prompt, ChatPromptTemplate)

    def test_split_zendesk_ticket_prompt_variables(self):
        """Test split Zendesk ticket prompt has required variables."""
        prompt = create_split_zendesk_ticket_prompt()

        required_vars = {"task", "chat_history"}
        assert required_vars.issubset(set(prompt.input_variables))

    def test_split_zendesk_ticket_prompt_structure(self):
        """Test the structure of split Zendesk ticket prompt."""
        prompt = create_split_zendesk_ticket_prompt()

        # Should have system, chat history, and human messages
        assert len(prompt.messages) == 3

        message_types = [msg.__class__.__name__ for msg in prompt.messages]
        assert "SystemMessagePromptTemplate" in message_types
        assert "MessagesPlaceholder" in message_types
        assert "HumanMessagePromptTemplate" in message_types

    def test_split_zendesk_ticket_prompt_customer_support_context(self):
        """Test split Zendesk ticket prompt has customer support context."""
        prompt = create_split_zendesk_ticket_prompt()

        test_data = {
            "task": "I need help with my order and also want to change my address",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should reference customer support context
        assert "customer support" in formatted.lower()
        assert "ticket" in formatted.lower()

    def test_split_zendesk_ticket_prompt_language_preservation(self):
        """Test split Zendesk ticket prompt preserves original language."""
        prompt = create_split_zendesk_ticket_prompt()

        test_data = {
            "task": "Bonjour, j'ai un problème avec ma commande",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should preserve language
        assert "same language" in formatted.lower()
        assert "input ticket" in formatted.lower()

    def test_split_zendesk_ticket_prompt_task_splitting(self):
        """Test split Zendesk ticket prompt splits multiple issues."""
        prompt = create_split_zendesk_ticket_prompt()

        test_data = {
            "task": "My account is locked and I can't reset my password. Also, I was charged twice for the same order.",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should handle multiple issues
        assert "different tasks" in formatted.lower()
        assert "split the input into multiple tasks" in formatted.lower()
        assert "account is locked" in formatted
        assert "charged twice" in formatted

    def test_split_zendesk_ticket_prompt_standalone_requirement(self):
        """Test split Zendesk ticket prompt creates standalone tasks."""
        prompt = create_split_zendesk_ticket_prompt()

        test_data = {
            "task": "I'm still having the same issue we discussed earlier",
            "chat_history": [
                {"role": "user", "content": "Login problems"},
                {"role": "assistant", "content": "Try clearing cache"},
            ],
        }

        formatted = prompt.format(**test_data)

        # Should create standalone tasks
        assert "standalone" in formatted.lower()
        assert "self-contained" in formatted.lower()
        assert "without the chat history" in formatted.lower()

    def test_split_zendesk_ticket_prompt_no_solution_attempt(self):
        """Test split Zendesk ticket prompt doesn't attempt solutions."""
        prompt = create_split_zendesk_ticket_prompt()

        test_data = {"task": "How do I cancel my subscription?", "chat_history": []}

        formatted = prompt.format(**test_data)

        # Should not attempt to solve
        assert "do not try to solve" in formatted.lower()
        assert "not suggest or generate new tasks" in formatted.lower()

    def test_split_zendesk_ticket_prompt_fallback_behavior(self):
        """Test split Zendesk ticket prompt fallback behavior."""
        prompt = create_split_zendesk_ticket_prompt()

        test_data = {"task": "Thank you for your assistance", "chat_history": []}

        formatted = prompt.format(**test_data)

        # Should have fallback
        assert "no tasks are found" in formatted.lower()
        assert "return the user input as is" in formatted.lower()

    def test_split_zendesk_ticket_prompt_with_mixed_language(self):
        """Test split Zendesk ticket prompt with mixed content."""
        prompt = create_split_zendesk_ticket_prompt()

        test_data = {
            "task": "Hello, I need help with order #12345. También tengo una pregunta sobre mi cuenta.",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should handle mixed content
        assert "order #12345" in formatted
        assert "También tengo una pregunta" in formatted


class TestTransformPromptsIntegration:
    """Test integration between transform prompts."""

    def test_all_prompts_are_chat_templates(self):
        """Test all transform prompts are ChatPromptTemplates."""
        prompts = [
            create_condense_task_prompt(),
            create_split_prompt(),
            create_split_zendesk_ticket_prompt(),
        ]

        for prompt in prompts:
            assert isinstance(prompt, ChatPromptTemplate)

    def test_prompts_have_chat_history_support(self):
        """Test all transform prompts support chat history."""
        prompts = [
            create_condense_task_prompt(),
            create_split_prompt(),
            create_split_zendesk_ticket_prompt(),
        ]

        for prompt in prompts:
            assert "chat_history" in prompt.input_variables

    def test_prompts_complement_each_other(self):
        """Test transform prompts can work in sequence."""
        condense_prompt = create_condense_task_prompt()
        split_prompt = create_split_prompt()

        # First, condense a task
        condensed = condense_prompt.format(
            task="Tell me more about that topic",
            chat_history=[
                {"role": "user", "content": "What is machine learning?"},
                {"role": "assistant", "content": "ML is..."},
            ],
        )

        # Then, split complex input
        split_result = split_prompt.format(
            user_input="Explain deep learning and neural networks. Also use simple language.",
            chat_history=[],
        )

        # Both should work with similar inputs
        assert isinstance(condensed, str)
        assert isinstance(split_result, str)

    def test_zendesk_vs_general_splitting(self):
        """Test differences between Zendesk and general splitting."""
        general_split = create_split_prompt()
        zendesk_split = create_split_zendesk_ticket_prompt()

        # General split should handle instructions
        general_formatted = general_split.format(
            user_input="Use formal language. What is the refund policy?",
            chat_history=[],
        )

        # Zendesk split focuses on customer issues
        zendesk_formatted = zendesk_split.format(
            task="What is the refund policy?", chat_history=[]
        )

        # General should mention instructions
        assert "instructions" in general_formatted.lower()

        # Zendesk should focus on customer support
        assert "customer support" in zendesk_formatted.lower()

    def test_transform_prompts_standalone_emphasis(self):
        """Test all transform prompts emphasize standalone outputs."""
        prompts = [
            create_condense_task_prompt(),
            create_split_prompt(),
            create_split_zendesk_ticket_prompt(),
        ]

        for prompt in prompts:
            formatted = prompt.format(
                **{
                    var: "test" if var != "chat_history" else []
                    for var in prompt.input_variables
                }
            )
            assert "standalone" in formatted.lower()

    def test_transform_prompts_no_generation_emphasis(self):
        """Test transform prompts emphasize not generating new content."""
        prompts = [
            create_condense_task_prompt(),
            create_split_prompt(),
            create_split_zendesk_ticket_prompt(),
        ]

        for prompt in prompts:
            formatted = prompt.format(
                **{
                    var: "test" if var != "chat_history" else []
                    for var in prompt.input_variables
                }
            )
            # Should contain some form of "don't generate/suggest new tasks"
            assert (
                "not suggest" in formatted.lower()
                or "not generate" in formatted.lower()
                or "do not" in formatted.lower()
            )
