def format_chat_history(history) -> list[tuple[str, str]]:
    """Format the chat history into a list of tuples (human, ai)"""

    return [(chat.user_message, chat.assistant) for chat in history]
