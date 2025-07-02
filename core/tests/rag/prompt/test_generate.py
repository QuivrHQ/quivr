"""Tests for generation prompts."""

from unittest.mock import patch
from langchain_core.prompts import ChatPromptTemplate

from quivr_core.rag.prompt.prompts.generate import (
    create_rag_answer_prompt,
    create_chat_llm_prompt,
    create_zendesk_template_prompt,
    create_zendesk_llm_prompt,
)


class TestRAGAnswerPrompt:
    """Test RAG answer generation prompt."""

    def test_create_rag_answer_prompt(self):
        """Test RAG answer prompt creation."""
        prompt = create_rag_answer_prompt()

        assert isinstance(prompt, ChatPromptTemplate)

    def test_rag_answer_prompt_variables(self):
        """Test RAG answer prompt has required variables."""
        prompt = create_rag_answer_prompt()

        required_vars = {
            "custom_instructions",
            "context",
            "files",
            "chat_history",
            "task",
            "rephrased_task",
        }
        assert required_vars.issubset(set(prompt.input_variables))

    def test_rag_answer_prompt_structure(self):
        """Test the structure of RAG answer prompt."""
        prompt = create_rag_answer_prompt()

        # Should have system, chat history, system, and human messages
        assert len(prompt.messages) >= 3

        message_types = [msg.__class__.__name__ for msg in prompt.messages]
        assert "SystemMessagePromptTemplate" in message_types
        assert "MessagesPlaceholder" in message_types
        assert "HumanMessagePromptTemplate" in message_types

    def test_rag_answer_prompt_quivr_identity(self):
        """Test RAG answer prompt identifies as Quivr."""
        prompt = create_rag_answer_prompt()

        test_data = {
            "custom_instructions": "",
            "context": "",
            "files": "",
            "chat_history": [],
            "task": "test task",
            "rephrased_task": "test task",
        }

        formatted = prompt.format(**test_data)
        assert "Quivr" in formatted

    @patch("quivr_core.rag.prompt.prompts.generate.datetime")
    def test_rag_answer_prompt_date_inclusion(self, mock_datetime):
        """Test RAG answer prompt includes current date."""
        mock_datetime.datetime.now.return_value.strftime.return_value = (
            "January 15, 2024"
        )

        prompt = create_rag_answer_prompt()

        test_data = {
            "custom_instructions": "",
            "context": "",
            "files": "",
            "chat_history": [],
            "task": "test",
            "rephrased_task": "test",
        }

        formatted = prompt.format(**test_data)
        assert "January 15, 2024" in formatted

    def test_rag_answer_prompt_instructions(self):
        """Test RAG answer prompt contains key instructions."""
        prompt = create_rag_answer_prompt()

        test_data = {
            "custom_instructions": "Be concise",
            "context": "Sample context",
            "files": "file1.txt, file2.txt",
            "chat_history": [],
            "task": "Summarize the content",
            "rephrased_task": "Provide a summary of the content",
        }

        formatted = prompt.format(**test_data)

        # Should contain key instructions
        assert "markdown" in formatted.lower()
        assert "provided context" in formatted.lower()
        assert "citing" in formatted.lower() or "cite" in formatted.lower()

    def test_rag_answer_prompt_context_only_instruction(self):
        """Test RAG answer prompt emphasizes using only provided context."""
        prompt = create_rag_answer_prompt()

        test_data = {
            "custom_instructions": "",
            "context": "Only this context should be used",
            "files": "",
            "chat_history": [],
            "task": "Answer question",
            "rephrased_task": "Answer the question",
        }

        formatted = prompt.format(**test_data)

        assert "ONLY the provided context" in formatted

    def test_rag_answer_prompt_with_files(self):
        """Test RAG answer prompt handles file information."""
        prompt = create_rag_answer_prompt()

        test_data = {
            "custom_instructions": "",
            "context": "Context from files",
            "files": "document1.pdf, document2.txt, spreadsheet.xlsx",
            "chat_history": [],
            "task": "Analyze documents",
            "rephrased_task": "Analyze the provided documents",
        }

        formatted = prompt.format(**test_data)

        assert "document1.pdf" in formatted
        assert "document2.txt" in formatted
        assert "spreadsheet.xlsx" in formatted

    def test_rag_answer_prompt_with_chat_history(self):
        """Test RAG answer prompt with chat history."""
        prompt = create_rag_answer_prompt()

        test_data = {
            "custom_instructions": "",
            "context": "Current context",
            "files": "",
            "chat_history": [
                {"role": "user", "content": "Previous question"},
                {"role": "assistant", "content": "Previous answer"},
            ],
            "task": "Follow-up question",
            "rephrased_task": "Answer the follow-up question",
        }

        formatted = prompt.format(**test_data)

        # Should handle chat history
        assert isinstance(formatted, str)
        assert "Follow-up question" in formatted

    def test_rag_answer_prompt_task_completion(self):
        """Test RAG answer prompt emphasizes completing all tasks."""
        prompt = create_rag_answer_prompt()

        test_data = {
            "custom_instructions": "",
            "context": "Context for tasks",
            "files": "",
            "chat_history": [],
            "task": "Task 1: Do this. Task 2: Do that.",
            "rephrased_task": "Complete both tasks",
        }

        formatted = prompt.format(**test_data)

        assert "ALL tasks" in formatted or "complete all" in formatted.lower()

    def test_rag_answer_prompt_conflicting_info_handling(self):
        """Test RAG answer prompt handles conflicting information."""
        prompt = create_rag_answer_prompt()

        test_data = {
            "custom_instructions": "",
            "context": "Conflicting information present",
            "files": "",
            "chat_history": [],
            "task": "Resolve conflicts",
            "rephrased_task": "Handle conflicting information",
        }

        formatted = prompt.format(**test_data)

        assert (
            "contradictory" in formatted.lower() or "conflicting" in formatted.lower()
        )


class TestChatLLMPrompt:
    """Test direct chat LLM prompt."""

    def test_create_chat_llm_prompt(self):
        """Test chat LLM prompt creation."""
        prompt = create_chat_llm_prompt()

        assert isinstance(prompt, ChatPromptTemplate)

    def test_chat_llm_prompt_variables(self):
        """Test chat LLM prompt has required variables."""
        prompt = create_chat_llm_prompt()

        required_vars = {"custom_instructions", "task", "chat_history"}
        assert required_vars.issubset(set(prompt.input_variables))

    def test_chat_llm_prompt_structure(self):
        """Test the structure of chat LLM prompt."""
        prompt = create_chat_llm_prompt()

        # Should have system, chat history, and human messages
        assert len(prompt.messages) >= 3

        message_types = [msg.__class__.__name__ for msg in prompt.messages]
        assert "SystemMessagePromptTemplate" in message_types
        assert "MessagesPlaceholder" in message_types
        assert "HumanMessagePromptTemplate" in message_types

    @patch("quivr_core.rag.prompt.prompts.generate.datetime")
    def test_chat_llm_prompt_date_inclusion(self, mock_datetime):
        """Test chat LLM prompt includes current date."""
        mock_datetime.datetime.now.return_value.strftime.return_value = "March 20, 2024"

        prompt = create_chat_llm_prompt()

        test_data = {"custom_instructions": "", "task": "test task", "chat_history": []}

        formatted = prompt.format(**test_data)
        assert "March 20, 2024" in formatted

    def test_chat_llm_prompt_quivr_identity(self):
        """Test chat LLM prompt identifies as Quivr."""
        prompt = create_chat_llm_prompt()

        test_data = {"custom_instructions": "", "task": "Hello", "chat_history": []}

        formatted = prompt.format(**test_data)
        assert "Quivr" in formatted

    def test_chat_llm_prompt_custom_instructions(self):
        """Test chat LLM prompt handles custom instructions."""
        prompt = create_chat_llm_prompt()

        test_data = {
            "custom_instructions": "Always respond in bullet points",
            "task": "Explain AI",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        assert "bullet points" in formatted
        assert "Explain AI" in formatted

    def test_chat_llm_prompt_no_custom_instructions(self):
        """Test chat LLM prompt with no custom instructions."""
        prompt = create_chat_llm_prompt()

        test_data = {
            "custom_instructions": None,
            "task": "Simple task",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        # Should handle None instructions gracefully
        assert "Simple task" in formatted


class TestZendeskTemplatePrompt:
    """Test Zendesk template prompt."""

    def test_create_zendesk_template_prompt(self):
        """Test Zendesk template prompt creation."""
        prompt = create_zendesk_template_prompt()

        assert isinstance(prompt, ChatPromptTemplate)

    def test_zendesk_template_prompt_variables(self):
        """Test Zendesk template prompt has required variables."""
        prompt = create_zendesk_template_prompt()

        required_vars = {
            "current_time",
            "guidelines",
            "user_metadata",
            "ticket_metadata",
            "similar_tickets",
            "ticket_history",
            "additional_information",
            "client_query",
        }
        assert required_vars.issubset(set(prompt.input_variables))

    def test_zendesk_template_prompt_structure(self):
        """Test the structure of Zendesk template prompt."""
        prompt = create_zendesk_template_prompt()

        # Should have system and human messages
        assert len(prompt.messages) == 2

        message_types = [msg.__class__.__name__ for msg in prompt.messages]
        assert "SystemMessagePromptTemplate" in message_types
        assert "HumanMessagePromptTemplate" in message_types

    def test_zendesk_template_prompt_customer_service_context(self):
        """Test Zendesk template prompt contains customer service context."""
        prompt = create_zendesk_template_prompt()

        test_data = {
            "current_time": "2024-01-15 10:30:00",
            "guidelines": "Be helpful and professional",
            "user_metadata": "Premium customer",
            "ticket_metadata": "Priority: High",
            "similar_tickets": "No similar tickets",
            "ticket_history": "First contact",
            "additional_information": "None",
            "client_query": "Need help with product",
        }

        formatted = prompt.format(**test_data)

        assert "Customer Service" in formatted
        assert "Zendesk" in formatted

    def test_zendesk_template_prompt_instructions(self):
        """Test Zendesk template prompt contains proper instructions."""
        prompt = create_zendesk_template_prompt()

        test_data = {
            "current_time": "2024-01-15 10:30:00",
            "guidelines": "Custom guidelines for responses",
            "user_metadata": "User info",
            "ticket_metadata": "Ticket info",
            "similar_tickets": "Similar cases",
            "ticket_history": "Previous interactions",
            "additional_information": "API data",
            "client_query": "Customer question",
        }

        formatted = prompt.format(**test_data)

        # Should contain formatting and behavior instructions
        assert "verbose" in formatted.lower()
        assert "format" in formatted.lower()
        assert "signature" in formatted.lower()

    def test_zendesk_template_prompt_time_handling(self):
        """Test Zendesk template prompt handles time information."""
        prompt = create_zendesk_template_prompt()

        test_data = {
            "current_time": "2024-03-15 14:45:30 UTC",
            "guidelines": "",
            "user_metadata": "",
            "ticket_metadata": "",
            "similar_tickets": "",
            "ticket_history": "",
            "additional_information": "",
            "client_query": "Time-sensitive request",
        }

        formatted = prompt.format(**test_data)

        assert "2024-03-15 14:45:30 UTC" in formatted

    def test_zendesk_template_prompt_guidelines_priority(self):
        """Test Zendesk template prompt prioritizes custom guidelines."""
        prompt = create_zendesk_template_prompt()

        test_data = {
            "current_time": "2024-01-15 10:00:00",
            "guidelines": "ALWAYS use formal language and include order numbers",
            "user_metadata": "",
            "ticket_metadata": "",
            "similar_tickets": "",
            "ticket_history": "",
            "additional_information": "",
            "client_query": "Order status inquiry",
        }

        formatted = prompt.format(**test_data)

        assert "ALWAYS use formal language" in formatted
        assert "order numbers" in formatted
        assert "prioritize" in formatted.lower() or "must follow" in formatted.lower()


class TestZendeskLLMPrompt:
    """Test Zendesk LLM prompt."""

    def test_create_zendesk_llm_prompt(self):
        """Test Zendesk LLM prompt creation."""
        prompt = create_zendesk_llm_prompt()

        assert isinstance(prompt, ChatPromptTemplate)

    def test_zendesk_llm_prompt_variables(self):
        """Test Zendesk LLM prompt has required variables."""
        prompt = create_zendesk_llm_prompt()

        required_vars = {"enforced_system_prompt", "task", "chat_history"}
        assert required_vars.issubset(set(prompt.input_variables))

    def test_zendesk_llm_prompt_structure(self):
        """Test the structure of Zendesk LLM prompt."""
        prompt = create_zendesk_llm_prompt()

        # Should have system, chat history, and human messages
        assert len(prompt.messages) == 3

        message_types = [msg.__class__.__name__ for msg in prompt.messages]
        assert "SystemMessagePromptTemplate" in message_types
        assert "MessagesPlaceholder" in message_types
        assert "HumanMessagePromptTemplate" in message_types

    def test_zendesk_llm_prompt_draft_handling(self):
        """Test Zendesk LLM prompt handles draft answers."""
        prompt = create_zendesk_llm_prompt()

        test_data = {
            "enforced_system_prompt": "System instructions",
            "task": "Thank you for contacting us. We will resolve your issue promptly.",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        assert "draft answer" in formatted.lower()
        assert "Thank you for contacting us" in formatted

    def test_zendesk_llm_prompt_system_enforcement(self):
        """Test Zendesk LLM prompt enforces system prompt."""
        prompt = create_zendesk_llm_prompt()

        test_data = {
            "enforced_system_prompt": "CRITICAL: Always include disclaimer",
            "task": "Draft response about refunds",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        assert "CRITICAL: Always include disclaimer" in formatted

    def test_zendesk_llm_prompt_ready_to_send(self):
        """Test Zendesk LLM prompt produces ready-to-send messages."""
        prompt = create_zendesk_llm_prompt()

        test_data = {
            "enforced_system_prompt": "Professional tone required",
            "task": "Response about product availability",
            "chat_history": [],
        }

        formatted = prompt.format(**test_data)

        assert "ready to be sent" in formatted


class TestGeneratePromptsIntegration:
    """Test integration between generation prompts."""

    def test_all_prompts_are_chat_templates(self):
        """Test all generation prompts are ChatPromptTemplates."""
        prompts = [
            create_rag_answer_prompt(),
            create_chat_llm_prompt(),
            create_zendesk_template_prompt(),
            create_zendesk_llm_prompt(),
        ]

        for prompt in prompts:
            assert isinstance(prompt, ChatPromptTemplate)

    def test_prompts_have_different_complexities(self):
        """Test prompts have appropriate complexity for their use cases."""
        rag_prompt = create_rag_answer_prompt()
        chat_prompt = create_chat_llm_prompt()
        zendesk_template = create_zendesk_template_prompt()
        zendesk_llm = create_zendesk_llm_prompt()

        # RAG should be most complex (most variables)
        assert len(rag_prompt.input_variables) >= len(chat_prompt.input_variables)

        # Zendesk template should be very specific (many variables)
        assert len(zendesk_template.input_variables) > len(zendesk_llm.input_variables)

    def test_quivr_identity_consistency(self):
        """Test that Quivr identity is consistent across prompts."""
        rag_prompt = create_rag_answer_prompt()
        chat_prompt = create_chat_llm_prompt()

        rag_formatted = rag_prompt.format(
            custom_instructions="",
            context="",
            files="",
            chat_history=[],
            task="test",
            rephrased_task="test",
        )

        chat_formatted = chat_prompt.format(
            custom_instructions="", task="test", chat_history=[]
        )

        # Both should identify as Quivr
        assert "Quivr" in rag_formatted
        assert "Quivr" in chat_formatted

    @patch("quivr_core.rag.prompt.prompts.generate.datetime")
    def test_date_consistency(self, mock_datetime):
        """Test that date formatting is consistent across prompts."""
        mock_datetime.datetime.now.return_value.strftime.return_value = "April 1, 2024"

        rag_prompt = create_rag_answer_prompt()
        chat_prompt = create_chat_llm_prompt()

        rag_formatted = rag_prompt.format(
            custom_instructions="",
            context="",
            files="",
            chat_history=[],
            task="test",
            rephrased_task="test",
        )

        chat_formatted = chat_prompt.format(
            custom_instructions="", task="test", chat_history=[]
        )

        # Both should have the same date format
        assert "April 1, 2024" in rag_formatted
        assert "April 1, 2024" in chat_formatted
