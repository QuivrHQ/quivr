"""
Transform prompts for input processing and task manipulation.

This module contains prompts that transform user input in various ways,
such as condensing tasks, splitting complex inputs, and reformatting content.
"""

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)

from quivr_core.rag.prompt.registry import register_prompt


@register_prompt(
    name="condense_task",
    description="Rephrases tasks to be standalone without chat history context",
    category="transform",
    tags=["task", "context", "reformulation", "standalone"],
)
def create_condense_task_prompt():
    """
    Creates a prompt for task rephrasing.

    Given a chat history and the latest user task which might reference context
    in the chat history, formulates a standalone task which can be understood
    without the chat history.
    """
    system_message_template = (
        "Given a chat history and the latest user task "
        "which might reference context in the chat history, "
        "formulate a standalone task which can be understood "
        "without the chat history. Do NOT complete the task, "
        "just reformulate it if needed and otherwise return it as is. "
        "Do not output your reasoning, just the task."
    )

    template_answer = "User task: {task}\n Standalone task:"

    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )


@register_prompt(
    name="split_input",
    description="Splits user input into multiple tasks and instructions",
    category="transform",
    tags=["task", "splitting", "instructions", "decomposition"],
)
def create_split_prompt():
    """
    Creates a prompt to split user input into multiple questions/instructions.

    Separates instructions (system behavior directives) from tasks (questions,
    summarization, translation, etc.) and ensures each is standalone.
    """
    system_message_template = (
        "Given a chat history and the user input, split and rephrase the input into instructions and tasks.\n"
        "- Instructions direct the system to behave in a certain way or to use specific tools: examples of instructions are "
        "'Can you reply in French?', 'Answer in French', 'You are an expert legal assistant', "
        "'You will behave as...', 'Use web search').\n"
        "- You shall collect and condense all the instructions into a single string.\n"
        "- The instructions shall be standalone and self-contained, so that they can be understood "
        "without the chat history. If no instructions are found, return an empty string.\n"
        "- Instructions to be understood may require considering the chat history.\n"
        "- Tasks are often questions, but they can also be summarisation tasks, translation tasks, content generation tasks, etc.\n"
        "- Tasks to be understood may require considering the chat history.\n"
        "- If the user input contains different tasks, you shall split the input into multiple tasks.\n"
        "- Each splitted task shall be a standalone, self-contained task which can be understood "
        "without the chat history. You shall rephrase the tasks if needed.\n"
        "- If no explicit task is present, you shall infer the tasks from the user input and the chat history.\n"
        "- Do NOT try to solve the tasks or answer the questions, "
        "just reformulate them if needed and otherwise return them as is.\n"
        "- Remember, you shall NOT suggest or generate new tasks.\n"
        "- As an example, the user input 'What is Apple? Who is its CEO? When was it founded?' "
        "shall be split into a list of tasks ['What is Apple?', 'Who is the CEO of Apple?', 'When was Apple founded?']\n"
        "- If no tasks are found, return the user input as is in the task list.\n"
    )

    template_answer = "User input: {user_input}"

    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )


@register_prompt(
    name="split_zendesk_ticket",
    description="Splits Zendesk tickets into multiple tasks maintaining original language",
    category="transform",
    tags=["zendesk", "ticket", "splitting", "customer_service", "multilingual"],
)
def create_split_zendesk_ticket_prompt():
    """
    Creates a prompt to split a Zendesk input ticket into multiple questions/tasks.

    Similar to split_input but specifically designed for customer support tickets,
    maintaining the original language of the ticket.
    """
    system_message_template = (
        "Given a chat history and an input customer support ticket, split and rephrase the ticket into multiple questions/tasks.\n"
        "- Tasks to be understood may require considering the chat history.\n"
        "- If the user input contains different tasks, you shall split the input into multiple tasks.\n"
        "- Each splitted task shall be a standalone, self-contained task which can be understood "
        "without the chat history. You shall rephrase the tasks if needed.\n"
        "- Do NOT try to solve the tasks or answer the questions, "
        "just reformulate them if needed and otherwise return them as is.\n"
        "- Remember, you shall NOT suggest or generate new tasks.\n"
        "- If no tasks are found, return the user input as is in the task list.\n"
        "- Use the same language as the input ticket.\n"
    )

    template_answer = "Input: {task}"

    return ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )
