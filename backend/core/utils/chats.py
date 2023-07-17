from logger import get_logger
from models.chats import ChatMessage
from models.settings import common_dependencies

logger = get_logger(__name__)


def get_chat_name_from_first_question(chat_message: ChatMessage):
    # Step 1: Get the summary of the first question
    # first_question_summary = summarize_as_title(chat_message.question)
    # Step 2: Process this summary to create a chat name by selecting the first three words
    chat_name = " ".join(chat_message.question.split()[:3])

    return chat_name
