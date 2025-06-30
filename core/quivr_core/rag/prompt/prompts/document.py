"""
Document formatting prompts for content presentation.

This module contains prompts that handle document formatting,
presentation, and content structuring for retrieval systems.
"""

from langchain_core.prompts import PromptTemplate

from quivr_core.rag.prompt.registry import register_prompt


@register_prompt(
    name="default_document",
    description="Formats document content with filename and source information",
    category="document",
    tags=["document", "formatting", "source", "metadata"],
)
def create_default_document_prompt():
    """
    Creates a prompt for formatting documents.

    Provides a standard template for presenting document content
    with associated metadata like filename and source information.
    """
    return PromptTemplate.from_template(
        template="Filename: {original_file_name}\nSource: {index} \n {page_content}"
    )
