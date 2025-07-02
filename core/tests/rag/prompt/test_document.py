"""Tests for document formatting prompts."""

import pytest
from langchain_core.prompts import PromptTemplate

from quivr_core.rag.prompt.prompts.document import create_default_document_prompt


class TestDefaultDocumentPrompt:
    """Test default document formatting prompt."""

    def test_create_default_document_prompt(self):
        """Test default document prompt creation."""
        prompt = create_default_document_prompt()

        assert isinstance(prompt, PromptTemplate)

    def test_default_document_prompt_variables(self):
        """Test default document prompt has required variables."""
        prompt = create_default_document_prompt()

        required_vars = {"original_file_name", "index", "page_content"}
        assert required_vars.issubset(set(prompt.input_variables))

    def test_default_document_prompt_formatting(self):
        """Test default document prompt formatting."""
        prompt = create_default_document_prompt()

        test_data = {
            "original_file_name": "test_document.pdf",
            "index": 1,
            "page_content": "This is sample document content with important information.",
        }

        formatted = prompt.format(**test_data)

        # Should contain all provided information
        assert "test_document.pdf" in formatted
        assert "1" in formatted
        assert "This is sample document content" in formatted

    def test_default_document_prompt_structure(self):
        """Test the structure of default document prompt."""
        prompt = create_default_document_prompt()

        test_data = {
            "original_file_name": "example.txt",
            "index": 5,
            "page_content": "Sample content",
        }

        formatted = prompt.format(**test_data)

        # Should follow expected structure
        assert "Filename:" in formatted
        assert "Source:" in formatted
        assert formatted.count("\n") >= 2  # Should have line breaks

    def test_default_document_prompt_with_special_characters(self):
        """Test document prompt with special characters."""
        prompt = create_default_document_prompt()

        test_data = {
            "original_file_name": "file with spaces & symbols.pdf",
            "index": 10,
            "page_content": "Content with symbols: @#$%^&*()_+-={}[]|\\:;\"'<>,.?/",
        }

        formatted = prompt.format(**test_data)

        # Should handle special characters
        assert "file with spaces & symbols.pdf" in formatted
        assert "@#$%^&*()_+-=" in formatted

    def test_default_document_prompt_with_empty_content(self):
        """Test document prompt with empty content."""
        prompt = create_default_document_prompt()

        test_data = {"original_file_name": "empty.txt", "index": 0, "page_content": ""}

        formatted = prompt.format(**test_data)

        # Should still format correctly with empty content
        assert "empty.txt" in formatted
        assert "0" in formatted

    def test_default_document_prompt_with_long_content(self):
        """Test document prompt with long content."""
        prompt = create_default_document_prompt()

        long_content = "This is a very long document content. " * 100
        test_data = {
            "original_file_name": "long_document.pdf",
            "index": 999,
            "page_content": long_content,
        }

        formatted = prompt.format(**test_data)

        # Should handle long content
        assert "long_document.pdf" in formatted
        assert "999" in formatted
        assert len(formatted) > 1000

    def test_default_document_prompt_with_multiline_content(self):
        """Test document prompt with multiline content."""
        prompt = create_default_document_prompt()

        multiline_content = """Line 1 of the document
Line 2 with different content
Line 3 with more information
Final line of the document"""

        test_data = {
            "original_file_name": "multiline.txt",
            "index": 42,
            "page_content": multiline_content,
        }

        formatted = prompt.format(**test_data)

        # Should preserve multiline content
        assert "multiline.txt" in formatted
        assert "42" in formatted
        assert "Line 1 of the document" in formatted
        assert "Final line of the document" in formatted

    def test_default_document_prompt_missing_variables(self):
        """Test document prompt with missing variables."""
        prompt = create_default_document_prompt()

        # Missing required variables should raise KeyError
        with pytest.raises(KeyError):
            prompt.format(original_file_name="test.pdf")  # Missing other vars

    def test_default_document_prompt_extra_variables(self):
        """Test document prompt ignores extra variables."""
        prompt = create_default_document_prompt()

        test_data = {
            "original_file_name": "test.pdf",
            "index": 1,
            "page_content": "content",
            "extra_var": "should be ignored",
            "another_extra": 123,
        }

        # Should not raise error with extra variables
        formatted = prompt.format(**test_data)
        assert isinstance(formatted, str)
        assert "test.pdf" in formatted

    def test_default_document_prompt_with_unicode(self):
        """Test document prompt with unicode characters."""
        prompt = create_default_document_prompt()

        test_data = {
            "original_file_name": "文档.pdf",  # Chinese characters
            "index": 1,
            "page_content": "Content with émojis 🎉 and ñoñó characters",
        }

        formatted = prompt.format(**test_data)

        # Should handle unicode correctly
        assert "文档.pdf" in formatted
        assert "🎉" in formatted
        assert "ñoñó" in formatted

    def test_default_document_prompt_consistent_formatting(self):
        """Test document prompt produces consistent formatting."""
        prompt = create_default_document_prompt()

        test_data = {
            "original_file_name": "consistency_test.pdf",
            "index": 100,
            "page_content": "Testing consistency",
        }

        # Format multiple times
        formatted1 = prompt.format(**test_data)
        formatted2 = prompt.format(**test_data)

        # Should be identical
        assert formatted1 == formatted2

    def test_default_document_prompt_template_structure(self):
        """Test the actual template structure."""
        prompt = create_default_document_prompt()

        # Check the template string directly
        template_str = prompt.template
        assert "Filename:" in template_str
        assert "Source:" in template_str
        assert "{original_file_name}" in template_str
        assert "{index}" in template_str
        assert "{page_content}" in template_str

    def test_default_document_prompt_variable_order(self):
        """Test that variables appear in expected order in formatted output."""
        prompt = create_default_document_prompt()

        test_data = {
            "original_file_name": "order_test.pdf",
            "index": 5,
            "page_content": "Content for order testing",
        }

        formatted = prompt.format(**test_data)

        # Filename should appear before Source, which should appear before content
        filename_pos = formatted.find("order_test.pdf")
        source_pos = formatted.find("5")
        content_pos = formatted.find("Content for order testing")

        assert filename_pos < source_pos < content_pos

    def test_default_document_prompt_edge_case_indices(self):
        """Test document prompt with edge case index values."""
        prompt = create_default_document_prompt()

        # Test with various index types
        test_cases = [
            {"index": 0, "desc": "zero index"},
            {"index": -1, "desc": "negative index"},
            {"index": 999999, "desc": "large index"},
        ]

        for case in test_cases:
            test_data = {
                "original_file_name": f"edge_case_{case['desc']}.pdf",
                "index": case["index"],
                "page_content": f"Content for {case['desc']}",
            }

            formatted = prompt.format(**test_data)
            assert str(case["index"]) in formatted
