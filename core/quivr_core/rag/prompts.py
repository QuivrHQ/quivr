import datetime
from pydantic import ConfigDict, create_model

from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder,
)


class CustomPromptsDict(dict):
    def __init__(self, type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type = type

    def __setitem__(self, key, value):
        # Automatically convert the value into a tuple (my_type, value)
        super().__setitem__(key, (self._type, value))


def _define_custom_prompts() -> CustomPromptsDict:
    custom_prompts: CustomPromptsDict = CustomPromptsDict(type=BasePromptTemplate)

    today_date = datetime.datetime.now().strftime("%B %d, %Y")

    # ---------------------------------------------------------------------------
    # Prompt for task rephrasing
    # ---------------------------------------------------------------------------
    system_message_template = (
        "Given a chat history and the latest user task "
        "which might reference context in the chat history, "
        "formulate a standalone task which can be understood "
        "without the chat history. Do NOT complete the task, "
        "just reformulate it if needed and otherwise return it as is. "
        "Do not output your reasoning, just the task."
    )

    template_answer = "User task: {task}\n Standalone task:"

    CONDENSE_TASK_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )

    custom_prompts["CONDENSE_TASK_PROMPT"] = CONDENSE_TASK_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt for RAG
    # ---------------------------------------------------------------------------
    system_message_template = f"Your name is Quivr. You're a helpful assistant. Today's date is {today_date}. "

    system_message_template += (
        "- When answering use markdown. Use markdown code blocks for code snippets.\n"
        "- Answer in a concise and clear manner.\n"
        "- If no preferred language is provided, answer in the same language as the language used by the user.\n"
        "- You must use ONLY the provided context to complete the task. "
        "Do not use any prior knowledge or external information, even if you are certain of the answer.\n"
        # "- If you cannot provide an answer using ONLY the context provided, do not attempt to answer from your own knowledge."
        # "Instead, inform the user that the answer isn't available in the context and suggest using the available tools {tools}.\n"
        "- Do not apologize when providing an answer.\n"
        "- Don't cite the source id in the answer objects, but you can use the source to complete the task.\n\n"
    )

    context_template = (
        "\n"
        # "- You have access to the following internal reasoning to provide an answer: {reasoning}\n"
        "- You have access to the following files to complete the task (limited to first 20 files): {files}\n"
        "- You have access to the following context to complete the task: {context}\n"
        "- Follow these user instruction when crafting the answer: {custom_instructions}\n"
        "- These user instructions shall take priority over any other previous instruction.\n"
        # "- Remember: if you cannot provide an answer using ONLY the provided context and CITING the sources, "
        # "inform the user that you don't have the answer and consider if any of the tools can help answer the question.\n"
        # "- Explain your reasoning about the potentiel tool usage in the answer.\n"
        # "- Only use binded tools to answer the question.\n"
        # "OFFER the user the possibility to ACTIVATE a relevant tool among "
        # "the tools which can be activated."
        # "Tools which can be activated: {tools}. If any of these tools can help in providing an answer "
        # "to the user question, you should offer the user the possibility to activate it. "
        # "Remember, you shall NOT use the above tools, ONLY offer the user the possibility to activate them.\n"
    )

    template_answer = (
        "Original task: {task}\n"
        "Rephrased and contextualized task: {rephrased_task}\n"
        "Remember, you shall complete ALL tasks.\n"
        "Remember: if you cannot provide an answer using ONLY the provided context and CITING the sources, "
        "just answer that you don't have the answer.\n"
        "If the provided context contains contradictory or conflicting information, state so providing the conflicting information.\n"
    )

    RAG_ANSWER_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            SystemMessagePromptTemplate.from_template(context_template),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )
    custom_prompts["RAG_ANSWER_PROMPT"] = RAG_ANSWER_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt for formatting documents
    # ---------------------------------------------------------------------------
    DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(
        template="Filename: {original_file_name}\nSource: {index} \n {page_content}"
    )
    custom_prompts["DEFAULT_DOCUMENT_PROMPT"] = DEFAULT_DOCUMENT_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt for chatting directly with LLMs, without any document retrieval stage
    # ---------------------------------------------------------------------------
    system_message_template = (
        f"Your name is Quivr. You're a helpful assistant. Today's date is {today_date}."
    )
    system_message_template += """
    If not None, also follow these user instructions when answering: {custom_instructions}
    """

    template_answer = """
    User Task: {task}
    Answer:
    """
    CHAT_LLM_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )
    custom_prompts["CHAT_LLM_PROMPT"] = CHAT_LLM_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt to understand the user intent
    # ---------------------------------------------------------------------------
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

    USER_INTENT_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )
    custom_prompts["USER_INTENT_PROMPT"] = USER_INTENT_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt to create a system prompt from user instructions
    # ---------------------------------------------------------------------------
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

    UPDATE_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )
    custom_prompts["UPDATE_PROMPT"] = UPDATE_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt to split the user input into multiple questions / instructions
    # ---------------------------------------------------------------------------
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

    SPLIT_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )
    custom_prompts["SPLIT_PROMPT"] = SPLIT_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt to grade the relevance of an answer and decide whather to perform a web search
    # ---------------------------------------------------------------------------
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

    TOOL_ROUTING_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            SystemMessagePromptTemplate.from_template(context_template),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )

    custom_prompts["TOOL_ROUTING_PROMPT"] = TOOL_ROUTING_PROMPT

    return custom_prompts


_custom_prompts = _define_custom_prompts()
CustomPromptsModel = create_model(
    "CustomPromptsModel", **_custom_prompts, __config__=ConfigDict(extra="forbid")
)

custom_prompts = CustomPromptsModel()
