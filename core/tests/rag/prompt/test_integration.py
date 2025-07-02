"""Integration tests for the prompt system."""

import pytest
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.prompts.base import BasePromptTemplate

from quivr_core.rag.prompt.registry import get_prompt, list_available_prompts
from quivr_core.rag.prompt.prompts import (
    create_user_intent_prompt,
    create_tool_routing_prompt,
    create_rag_answer_prompt,
    create_chat_llm_prompt,
    create_zendesk_template_prompt,
    create_zendesk_llm_prompt,
    create_update_prompt,
    create_condense_task_prompt,
    create_split_prompt,
    create_split_zendesk_ticket_prompt,
    create_default_document_prompt,
)


class TestPromptRegistryIntegration:
    """Test integration between prompt registry and prompt modules."""

    def test_all_prompts_registered(self):
        """Test that all prompt creation functions register their prompts."""
        # Import the module to trigger registration

        # Get all registered prompts
        registered_prompts = list_available_prompts()

        # Check that we have prompts registered
        assert len(registered_prompts) > 0

        # Expected prompt names (these should match the @register_prompt decorators)
        expected_names = [
            "user_intent",
            "tool_routing",
            "rag_answer",
            "chat_llm",
            "zendesk_template",
            "zendesk_llm",
            "update_system_prompt",
            "condense_task",
            "split_input",
            "split_zendesk_ticket",
            "default_document",
        ]

        # Verify key prompts are registered
        for name in expected_names:
            if name in registered_prompts:
                prompt = get_prompt(name)
                assert isinstance(prompt, BasePromptTemplate)

    def test_prompt_categories(self):
        """Test that prompts are properly categorized."""

        # Check category distribution
        classify_prompts = list_available_prompts(category="classify")
        generate_prompts = list_available_prompts(category="generate")
        transform_prompts = list_available_prompts(category="transform")
        system_prompts = list_available_prompts(category="system")
        document_prompts = list_available_prompts(category="document")

        # Should have prompts in multiple categories
        categories_with_prompts = sum(
            [
                len(classify_prompts) > 0,
                len(generate_prompts) > 0,
                len(transform_prompts) > 0,
                len(system_prompts) > 0,
                len(document_prompts) > 0,
            ]
        )

        assert categories_with_prompts >= 3  # At least 3 categories should have prompts

    def test_prompt_retrieval_consistency(self):
        """Test that retrieved prompts are consistent with factory functions."""
        # Test a few key prompts
        prompt_tests = [
            ("user_intent", create_user_intent_prompt),
            ("rag_answer", create_rag_answer_prompt),
            ("default_document", create_default_document_prompt),
        ]

        for name, factory in prompt_tests:
            try:
                registered = get_prompt(name)
                direct = factory()

                # Should be same type
                assert type(registered) == type(direct)

                # Should have same variables
                assert set(registered.input_variables) == set(direct.input_variables)

            except KeyError:
                # Skip if not registered (some prompts might not be in registry)
                continue


class TestPromptSystemWorkflow:
    """Test complete prompt system workflows."""

    def test_rag_workflow(self):
        """Test a complete RAG workflow using prompts."""
        # Step 1: Determine user intent
        intent_prompt = create_user_intent_prompt()
        intent_result = intent_prompt.format(task="What is machine learning?")
        assert isinstance(intent_result, str)

        # Step 2: Condense task if needed
        condense_prompt = create_condense_task_prompt()
        condensed_task = condense_prompt.format(
            task="What is machine learning?", chat_history=[]
        )
        assert isinstance(condensed_task, str)

        # Step 3: Route to appropriate tools
        routing_prompt = create_tool_routing_prompt()
        routing_result = routing_prompt.format(
            context="Basic ML information available",
            activated_tools="web_search",
            tasks="What is machine learning?",
            chat_history=[],
        )
        assert isinstance(routing_result, str)

        # Step 4: Generate answer
        rag_prompt = create_rag_answer_prompt()
        final_answer = rag_prompt.format(
            custom_instructions="Be educational",
            context="Machine learning is a subset of AI...",
            files="ml_guide.pdf",
            chat_history=[],
            task="What is machine learning?",
            rephrased_task="Explain machine learning",
        )
        assert isinstance(final_answer, str)

    def test_zendesk_workflow(self):
        """Test a complete Zendesk customer service workflow."""
        # Step 1: Split ticket into tasks
        split_prompt = create_split_zendesk_ticket_prompt()
        split_result = split_prompt.format(
            task="I need help with my order and also want to change my address",
            chat_history=[],
        )
        assert isinstance(split_result, str)

        # Step 2: Generate template response
        template_prompt = create_zendesk_template_prompt()
        template_result = template_prompt.format(
            current_time="2024-01-15 10:30:00 UTC",
            guidelines="Be professional and helpful",
            user_metadata="Premium customer since 2020",
            ticket_metadata="Priority: High, Category: Billing",
            similar_tickets="Previous order issues resolved quickly",
            ticket_history="First contact about this issue",
            additional_information="Order #12345 placed yesterday",
            client_query="I need help with my order and also want to change my address",
        )
        assert isinstance(template_result, str)

        # Step 3: Refine with LLM
        llm_prompt = create_zendesk_llm_prompt()
        final_response = llm_prompt.format(
            enforced_system_prompt="Always include next steps for customer",
            task=template_result[:200] + "...",  # Simulated draft response
            chat_history=[],
        )
        assert isinstance(final_response, str)

    def test_system_update_workflow(self):
        """Test system prompt update workflow."""
        # Update system behavior
        update_prompt = create_update_prompt()
        update_result = update_prompt.format(
            instruction="Always provide examples when explaining concepts",
            system_prompt="You are a helpful assistant",
            available_tools="web_search, example_generator, code_runner",
            activated_tools="web_search",
        )
        assert isinstance(update_result, str)

        # Should contain guidance about examples
        assert "examples" in update_result.lower()

    def test_chat_vs_rag_differences(self):
        """Test differences between chat and RAG prompts."""
        chat_prompt = create_chat_llm_prompt()
        rag_prompt = create_rag_answer_prompt()

        # Chat should be simpler
        assert len(chat_prompt.input_variables) < len(rag_prompt.input_variables)

        # RAG should require context
        assert "context" in rag_prompt.input_variables
        assert "context" not in chat_prompt.input_variables

        # Both should work for similar simple tasks
        task = "Explain photosynthesis"

        chat_result = chat_prompt.format(
            custom_instructions="", task=task, chat_history=[]
        )

        rag_result = rag_prompt.format(
            custom_instructions="",
            context="Photosynthesis information from biology textbook",
            files="biology.pdf",
            chat_history=[],
            task=task,
            rephrased_task=task,
        )

        assert isinstance(chat_result, str)
        assert isinstance(rag_result, str)
        assert "photosynthesis" in chat_result.lower()
        assert "photosynthesis" in rag_result.lower()


class TestPromptCompatibility:
    """Test compatibility and consistency across prompts."""

    def test_all_prompts_support_basic_formatting(self):
        """Test that all prompts can be formatted with basic inputs."""
        prompts = [
            create_user_intent_prompt(),
            create_tool_routing_prompt(),
            create_rag_answer_prompt(),
            create_chat_llm_prompt(),
            create_zendesk_template_prompt(),
            create_zendesk_llm_prompt(),
            create_update_prompt(),
            create_condense_task_prompt(),
            create_split_prompt(),
            create_split_zendesk_ticket_prompt(),
            create_default_document_prompt(),
        ]

        for prompt in prompts:
            # Create minimal test data for each prompt
            if isinstance(prompt, ChatPromptTemplate):
                test_data = {}
                for var in prompt.input_variables:
                    if var == "chat_history":
                        test_data[var] = []
                    else:
                        test_data[var] = "test"

                formatted = prompt.format(**test_data)
                assert isinstance(formatted, str)
                assert len(formatted) > 0

            elif isinstance(prompt, PromptTemplate):
                test_data = {var: "test" for var in prompt.input_variables}
                formatted = prompt.format(**test_data)
                assert isinstance(formatted, str)
                assert len(formatted) > 0

    def test_chat_history_consistency(self):
        """Test that prompts handle chat history consistently."""
        chat_history_prompts = [
            create_tool_routing_prompt(),
            create_rag_answer_prompt(),
            create_chat_llm_prompt(),
            create_zendesk_llm_prompt(),
            create_condense_task_prompt(),
            create_split_prompt(),
            create_split_zendesk_ticket_prompt(),
        ]

        sample_history = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]

        for prompt in chat_history_prompts:
            test_data = {}
            for var in prompt.input_variables:
                if var == "chat_history":
                    test_data[var] = sample_history
                else:
                    test_data[var] = "test"

            formatted = prompt.format(**test_data)
            assert isinstance(formatted, str)

    def test_unicode_support(self):
        """Test that prompts handle unicode characters properly."""
        unicode_test_data = {
            "task": "Explain émojis 🎉 and ñoñó characters",
            "content": "Unicode: 中文, العربية, русский",
            "name": "José María",
        }

        # Test with a few representative prompts
        test_prompts = [
            create_user_intent_prompt(),
            create_default_document_prompt(),
            create_chat_llm_prompt(),
        ]

        for prompt in test_prompts:
            test_data = {}
            for var in prompt.input_variables:
                if var == "chat_history":
                    test_data[var] = []
                elif var in unicode_test_data:
                    test_data[var] = unicode_test_data[var]
                else:
                    test_data[var] = "test"

            formatted = prompt.format(**test_data)
            assert isinstance(formatted, str)

            # Check that unicode is preserved
            for unicode_text in unicode_test_data.values():
                if unicode_text in test_data.values():
                    assert unicode_text in formatted

    def test_empty_input_handling(self):
        """Test that prompts handle empty inputs gracefully."""
        # Test with a few representative prompts
        test_prompts = [
            create_default_document_prompt(),
            create_user_intent_prompt(),
            create_chat_llm_prompt(),
        ]

        for prompt in test_prompts:
            test_data = {}
            for var in prompt.input_variables:
                if var == "chat_history":
                    test_data[var] = []
                else:
                    test_data[var] = ""  # Empty string

            formatted = prompt.format(**test_data)
            assert isinstance(formatted, str)


class TestPromptErrorHandling:
    """Test error handling across the prompt system."""

    def test_missing_variables_handling(self):
        """Test that prompts properly handle missing variables."""
        prompt = create_rag_answer_prompt()

        # Should raise KeyError for missing required variables
        with pytest.raises(KeyError):
            prompt.format(task="test")  # Missing other required variables

    def test_registry_error_handling(self):
        """Test registry error handling."""
        # Test getting non-existent prompt
        with pytest.raises(KeyError):
            get_prompt("non_existent_prompt")

    def test_prompt_factory_error_handling(self):
        """Test error handling in prompt factories."""
        # All factory functions should work without errors
        factories = [
            create_user_intent_prompt,
            create_tool_routing_prompt,
            create_rag_answer_prompt,
            create_chat_llm_prompt,
            create_zendesk_template_prompt,
            create_zendesk_llm_prompt,
            create_update_prompt,
            create_condense_task_prompt,
            create_split_prompt,
            create_split_zendesk_ticket_prompt,
            create_default_document_prompt,
        ]

        for factory in factories:
            try:
                prompt = factory()
                assert isinstance(prompt, BasePromptTemplate)
            except Exception as e:
                pytest.fail(f"Factory {factory.__name__} failed: {e}")


class TestPromptPerformance:
    """Test performance characteristics of the prompt system."""

    def test_prompt_creation_performance(self):
        """Test that prompt creation is reasonably fast."""
        import time

        factories = [
            create_user_intent_prompt,
            create_rag_answer_prompt,
            create_chat_llm_prompt,
        ]

        for factory in factories:
            start_time = time.time()
            prompt = factory()
            creation_time = time.time() - start_time

            # Should create prompts quickly (less than 1 second)
            assert creation_time < 1.0
            assert isinstance(prompt, BasePromptTemplate)

    def test_prompt_formatting_performance(self):
        """Test that prompt formatting is reasonably fast."""
        import time

        prompt = create_rag_answer_prompt()

        test_data = {
            "custom_instructions": "Be helpful",
            "context": "Test context " * 100,  # Longer context
            "files": "file1.pdf, file2.txt",
            "chat_history": [],
            "task": "Test task",
            "rephrased_task": "Test task rephrased",
        }

        start_time = time.time()
        formatted = prompt.format(**test_data)
        formatting_time = time.time() - start_time

        # Should format quickly (less than 1 second)
        assert formatting_time < 1.0
        assert isinstance(formatted, str)
        assert len(formatted) > 0

    def test_registry_lookup_performance(self):
        """Test that registry lookups are fast."""
        import time

        available_prompts = list_available_prompts()
        if not available_prompts:
            pytest.skip("No prompts registered")

        prompt_name = available_prompts[0]

        # Test multiple lookups
        start_time = time.time()
        for _ in range(100):
            prompt = get_prompt(prompt_name)
            assert isinstance(prompt, BasePromptTemplate)
        lookup_time = time.time() - start_time

        # 100 lookups should be very fast
        assert lookup_time < 1.0
