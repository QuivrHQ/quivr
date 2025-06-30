"""
System prompts for managing and updating system behavior.

This module contains prompts that handle system-level operations,
such as updating system prompts based on user instructions.
"""

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

from quivr_core.rag.prompt.registry import register_prompt


@register_prompt(
    name="update_system_prompt",
    description="Updates system prompts based on user instructions and tool availability",
    category="system",
    tags=["system", "update", "instructions", "tools", "prompt_engineering"],
)
def create_update_prompt():
    """
    Creates a prompt to update system prompts from user instructions.

    Takes user instructions and current system state to generate updated
    system prompts, managing tool activation and ensuring consistency
    with existing system behavior.
    """
    system_message_template = (
        "- Given the following user instruction, current system prompt, list of available tools "
        "and list of activated tools, update the prompt to include the instruction and decide which tools to activate.\n"
        "- The prompt shall only contain generic instructions which can be applied to any user task or question.\n"
        "- The prompt shall be concise and clear.\n"
        "- If the system prompt already contains the instruction, do not add it again.\n"
        "- If the system prompt contradicts ther user instruction, remove the contradictory "
        "statement or statements in the system prompt.\n"
        "- You shall return separately the updated system prompt and the reasoning that led to the update.\n"
        "- If the system prompt refers to a tool, you shall add the tool to the list of activated tools.\n"
        "- If no tool activation is needed, return empty lists.\n"
        "- You shall also return the reasoning that led to the tool activation.\n"
        "- Current system prompt: {system_prompt}\n"
        "- List of available tools: {available_tools}\n"
        "- List of activated tools: {activated_tools}\n\n"
    )

    template_answer = "User instructions: {instruction}\n"

    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )
