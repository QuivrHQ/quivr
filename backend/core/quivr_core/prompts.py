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
    # Prompt for question rephrasing
    # ---------------------------------------------------------------------------
    system_message_template = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is. "
        "Do not output your reasoning, just the question."
    )

    template_answer = "User question: {question}\n Standalone question:"

    CONDENSE_QUESTION_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )

    custom_prompts["CONDENSE_QUESTION_PROMPT"] = CONDENSE_QUESTION_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt for RAG
    # ---------------------------------------------------------------------------
    system_message_template = f"Your name is Quivr. You're a helpful assistant. Today's date is {today_date}. "

    system_message_template += (
        "When answering use markdown. Use markdown code blocks for code snippets. "
        "Answer in a concise and clear manner. "
        "Use the following pieces of context from the files provided by the user to answer the question. "
        "If no preferred language is provided, answer in the same language as the language used by the user. "
        "If you cannot provide an answer using only the context provided by the files, "
        "just say that you don't know the answer, don't try to make up an answer. "
        "Do not apologize when providing an answer. "
        "Don't cite the source id in the answer objects, but you can use the source to answer the question.\n"
    )

    context_template = (
        "You have access to the following files to answer the user question (limited to first 20 files): {files}\n"
        "Context: {context}\n"
        "Follow these user instruction when crafting the answer: {custom_instructions} "
        "These user instructions shall take priority over any other previous instruction.\n"
    )

    template_answer = "User question: {question}\n" "Answer:"

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
        template="Source: {index} \n {page_content}"
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
    User Question: {question}
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
        "execute a task:\n"
        "    - if the user is providing direct instructions to modify the system behaviour (for instance, "
        "'Can you reply in French?' or 'Answer in French' or 'You are an expert legal assistant' "
        "or 'You will behave as...'), the user intent is 'prompt';\n"
        "    - in all other cases (asking questions, asking for summarising a text, asking for translating a text, ...), "
        "the intent is 'task'.\n"
    )

    template_answer = "User input: {question}"

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
        "Given the following user instruction and the current system prompt, "
        "update the prompt to include the instruction. "
        "If the system prompt already contains the instruction, do not add it again. "
        "If the system prompt contradicts ther user instruction, remove the contradictory "
        "statement or statements in the system prompt. "
        "You shall return separately the updated system prompt and the reasoning that led to the update.\n"
        "Current system prompt: {system_prompt}\n"
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
        "Given a chat history and the latest user input split the input into instructions and tasks.\n"
        "Instructions direct the system to behave in a certain way: examples of instructions are "
        "'Can you reply in French?' or 'Answer in French' or 'You are an expert legal assistant' "
        "or 'You will behave as...'). You shall collect and condense all the instructions into a single string. "
        "The instructions should be standalone, self-contained instructions which can be understood "
        "without the chat history. If no instructions are found, return an empty string. \n"
        "Tasks are often questions, but they can also be summarisation tasks, translation tasks, content generation tasks, etc. "
        "If the user input contains different tasks, you shall split the input into multiple tasks. "
        "Each splitted task should be a standalone, self-contained task which can be understood "
        "without the chat history. Do NOT try to solve the tasks or answer the questions, "
        "just reformulate them if needed and otherwise return them as is. Do not output your reasoning, just the tasks. "
        "Remember, you shall NOT suggest or generate new tasks. "
        "As an example, the user input 'What is Apple? Who is its CEO? When was it founded?' "
        "shall be split into the questions 'What is Apple?', 'Who is the CEO of Apple?' and 'When was Apple founded?'.\n"
        "If no tasks are found, return the user input as is in the task .\n"
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
        "1) Consider each task separately,\n"
        "2) Determine whether the context and chat history contain "
        "all the information necessary to complete the task, "
        "or if a web search is necessary to gather more information.\n"
    )

    context_template = "Context: {context}\n"

    template_answer = "Tasks: {tasks}\n"

    WEBSEARCH_ROUTING_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
            SystemMessagePromptTemplate.from_template(context_template),
            HumanMessagePromptTemplate.from_template(template_answer),
        ]
    )

    custom_prompts["WEBSEARCH_ROUTING_PROMPT"] = WEBSEARCH_ROUTING_PROMPT

    return custom_prompts


_custom_prompts = _define_custom_prompts()
CustomPromptsModel = create_model(
    "CustomPromptsModel", **_custom_prompts, __config__=ConfigDict(extra="forbid")
)

custom_prompts = CustomPromptsModel()
