from typing import List, Tuple

from langchain.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage


def format_chat_history(history) -> List[Tuple[str, str]]:
    """Format the chat history into a list of tuples (human, ai)"""

    return [(chat.user_message, chat.assistant) for chat in history]


def format_history_to_openai_mesages(
    tuple_history: List[Tuple[str, str]], system_message: str, question: str
) -> List[BaseMessage]:
    """Format the chat history into a list of Base Messages"""
    messages = []
    messages.append(SystemMessage(content=system_message))
    for human, ai in tuple_history:
        messages.append(HumanMessage(content=human))
        messages.append(AIMessage(content=ai))
    messages.append(HumanMessage(content=question))
    return messages
