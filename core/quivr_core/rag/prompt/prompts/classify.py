"""
Classification prompts for intent detection and routing.

This module contains prompts that classify user input to determine intent,
route to appropriate tools, or categorize the type of request.
"""

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

from quivr_core.rag.prompt.registry import register_prompt


@register_prompt(
    name="user_intent",
    description="Determines if user input is instruction or task",
    category="classify",
    tags=["intent", "classification", "instruction", "task"],
)
def create_user_intent_prompt():
    """
    Creates a prompt to understand user intent.

    Determines whether the user is providing instructions to modify system
    behavior or asking the system to complete a task.
    """
    system_message_template = (
        "Given the following user input, determine the user intent, in particular "
        "whether the user is providing instructions to the system or is asking the system to "
        "complete a task:\n"
        "    - if the user is providing direct instructions to modify the system behaviour (for instance, "
        "'Can you reply in French?' or 'Answer in French' or 'You are an expert legal assistant' "
        "or 'You will behave as...'), the user intent is 'prompt';\n"
        "    - in all other cases (asking questions, asking for summarising a text, asking for translating a text, ...), "
        "the intent is 'task'.\n"
    )

    template_answer = "User input: {task}"

    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )


@register_prompt(
    name="tool_routing",
    description="Routes tasks to appropriate tools based on context availability",
    category="classify",
    tags=["routing", "tools", "context", "decision"],
)
def create_tool_routing_prompt():
    """
    Creates a prompt to grade relevance and decide on tool usage.

    Determines whether tasks can be completed with available context and chat
    history, or if external tools are needed. Routes to appropriate tools when
    context is insufficient.
    """
    system_message_template = (
        "Given the following tasks you shall determine whether all tasks can be "
        "completed fully and in the best possible way using the provided context and chat history. "
        "You shall:\n"
        "- Consider each task separately,\n"
        "- Determine whether the context and chat history contain "
        "all the information necessary to complete the task.\n"
        "- If the context and chat history do not contain all the information necessary to complete the task, "
        "consider ONLY the list of tools below and select the tool most appropriate to complete the task.\n"
        "- If no tools are listed, return the tasks as is and no tool.\n"
        "- If no relevant tool can be selected, return the tasks as is and no tool.\n"
        "- Do not propose to use a tool if that tool is not listed among the available tools.\n"
    )

    context_template = "Context: {context}\n {activated_tools}\n"
    template_answer = "Tasks: {tasks}\n"

    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            SystemMessagePromptTemplate.from_template(context_template),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )
