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
    _template = (
        "Given the following conversation and a follow up question, "
        "rephrase the follow up question to be a standalone question, "
        "in its original language. Keep as much details as possible from the chat history. "
        "Keep entity names and all.\n"
        "Chat history: {chat_history}\n"
        "Follow up question: {question}\n"
        "Standalone question:"
    )

    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)
    custom_prompts["CONDENSE_QUESTION_PROMPT"] = CONDENSE_QUESTION_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt for RAG
    # ---------------------------------------------------------------------------
    system_message_template = f"Your name is Quivr. You're a helpful assistant. Today's date is {today_date}. "

    system_message_template += (
        "When answering use markdown. "
        "Use markdown code blocks for code snippets. "
        "Answer in a concise and clear manner. "
        "Use the following pieces of context from the files provided by the user to answer the question. "
        "If no preferred language is provided, answer in the same language as the language used by the user."
        "If you cannot provide an answer using only the context provided by the files, "
        "just say that you don't know the answer, "
        "don't try to make up an answer. "
        "Don't cite the source id in the answer objects, but you can use the source to answer the question.\n"
        "You have access to the following files to answer the user question (limited to first 20 files): {files}\n"
        "Follow these user instruction when crafting the answer: {custom_instructions}. "
        "These user instructions shall take priority over any other previous instruction.\n"
    )

    template_answer = "Context: {context}\n" "User question: {question}\n" "Answer:"

    RAG_ANSWER_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(system_message_template),
            MessagesPlaceholder(variable_name="chat_history"),
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
    _template = (
        "Given the following user input, determine the user intent:\n"
        "    - if the user is providing direct instructions to the system (for instance, "
        "'Can you reply in French?' or 'Answer in French' or 'You are an expert legal assistant' "
        "or 'You will behave as...'), the user intent is 'prompt';\n"
        "    - in all other cases, the intent is 'rag';\n"
        "    - if you are unsure about the user intent, the itent is 'unsure';\n"
        "User input: {question}"
    )

    USER_INTENT_PROMPT = PromptTemplate.from_template(_template)
    custom_prompts["USER_INTENT_PROMPT"] = USER_INTENT_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt to create a system prompt from user instructions
    # ---------------------------------------------------------------------------
    _template = (
        "Given the following user instruction and the current system prompt, "
        "update the prompt to include the instruction. "
        "If the system prompt already contains the instruction, do not add it again. "
        "If the system prompt contradicts ther user instruction, remove the contradictory "
        "statement or statements in the system prompt.\n"
        "Current system prompt: {system_prompt}\n"
        "User instructions: {instruction}\n"
        "You shall return separately the updated system prompt and the reasoning that led to the update."
    )

    UPDATE_PROMPT = PromptTemplate.from_template(_template)
    custom_prompts["UPDATE_PROMPT"] = UPDATE_PROMPT

    # ---------------------------------------------------------------------------
    # Prompt to split the user input into multiple questions / instructions
    # ---------------------------------------------------------------------------
    _template = (
        "Given the following user input, split the input into instructions and questions. "
        "Instructions direct the system to behave in a certain way: examples of instructions are "
        "'Can you reply in French?' or 'Answer in French' or 'You are an expert legal assistant' "
        "or 'You will behave as...'). You shall collect and condense all the instructions into a single string. "
        "If no instructions are found, return an empty string. \n"
        "Questions, on the other hand, are questions that the system should answer. You shall determine if the user "
        "input contains different questions, in which case you shall split the user input into multiple questions. "
        "Each splitted question should be self-contained. "
        "As an example, the user input 'What is Apple and who is the CEO? shall be split into the two questions "
        "'What is Apple?' and 'Who is the CEO of Apple?'. "
        "If no questions are found, return an empty list. \n"
        "User input: {user_input}"
    )

    SPLIT_PROMPT = PromptTemplate.from_template(_template)
    custom_prompts["SPLIT_PROMPT"] = SPLIT_PROMPT

    return custom_prompts


_custom_prompts = _define_custom_prompts()
CustomPromptsModel = create_model(
    "CustomPromptsModel", **_custom_prompts, __config__=ConfigDict(extra="forbid")
)

custom_prompts = CustomPromptsModel()
