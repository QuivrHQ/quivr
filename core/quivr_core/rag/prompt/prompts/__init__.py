"""
Prompt modules for different categories.

This package contains categorized prompt modules that register themselves
with the prompt registry when imported.
"""

# Import all prompt modules to register them
# These imports are necessary for their side effects (registering prompts)
from . import transform  # noqa: F401
from . import classify  # noqa: F401
from . import generate  # noqa: F401
from . import system  # noqa: F401
from . import document  # noqa: F401

# Also expose individual functions for direct usage if needed
from .classify import create_user_intent_prompt, create_tool_routing_prompt
from .generate import (
    create_rag_answer_prompt,
    create_chat_llm_prompt,
    create_zendesk_template_prompt,
    create_zendesk_llm_prompt,
)
from .system import create_update_prompt
from .transform import (
    create_condense_task_prompt,
    create_split_prompt,
    create_split_zendesk_ticket_prompt,
)
from .document import create_default_document_prompt

__all__ = [
    # Individual prompt creation functions
    "create_user_intent_prompt",
    "create_tool_routing_prompt",
    "create_rag_answer_prompt",
    "create_chat_llm_prompt",
    "create_zendesk_template_prompt",
    "create_zendesk_llm_prompt",
    "create_update_prompt",
    "create_condense_task_prompt",
    "create_split_prompt",
    "create_split_zendesk_ticket_prompt",
    "create_default_document_prompt",
]
