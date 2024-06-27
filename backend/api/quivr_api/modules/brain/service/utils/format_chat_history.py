from typing import Dict, List, Tuple

from langchain.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage
from quivr_api.modules.chat.dto.outputs import GetChatHistoryOutput


def format_chat_history(
    history: List[GetChatHistoryOutput],
) -> List[Dict[str, str]]:
    """Format the chat history into a list of HumanMessage and AIMessage"""
    formatted_history = []
    for chat in history:
        if chat.user_message:
            formatted_history.append(HumanMessage(content=chat.user_message))
        if chat.assistant:
            formatted_history.append(AIMessage(content=chat.assistant))
    return formatted_history


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
