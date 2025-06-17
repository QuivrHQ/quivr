import logging
from langchain_core.prompts.base import BasePromptTemplate

from quivr_core.rag.prompts import custom_prompts, TemplatePromptName

logger = logging.getLogger("quivr_core")


class RAGPromptService:
    """Service for prompt template management and context building."""

    def __init__(self):
        self.templates = custom_prompts

    def get_template(self, template_name: TemplatePromptName) -> BasePromptTemplate:
        """
        Get a prompt template by name.

        Args:
            template_name: Name of the template to retrieve

        Returns:
            The prompt template
        """
        return self.templates[template_name]
