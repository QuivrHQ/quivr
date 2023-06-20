from logger import get_logger
from models.chats import ChatMessage
from models.settings import CommonsDep

logger = get_logger(__name__)


def create_chat(commons: CommonsDep, user_id, history, chat_name):
    # Chat is created upon the user's first question asked
    logger.info(f"New chat entry in chats table for user {user_id}")

    # Insert a new row into the chats table
    new_chat = {
        "user_id": user_id,
        "history": history,  # Empty chat to start
        "chat_name": chat_name,
    }
    insert_response = commons["supabase"].table("chats").insert(new_chat).execute()
    logger.info(f"Insert response {insert_response.data}")

    return insert_response


def update_chat(commons: CommonsDep, chat_id, history=None, chat_name=None):
    if not chat_id:
        logger.error("No chat_id provided")
        return

    updates = {}

    if history is not None:
        updates["history"] = history

    if chat_name is not None:
        updates["chat_name"] = chat_name

    if updates:
        commons["supabase"].table("chats").update(updates).match(
            {"chat_id": chat_id}
        ).execute()
        logger.info(f"Chat {chat_id} updated")
    else:
        logger.info(f"No updates to apply for chat {chat_id}")


def get_chat_name_from_first_question(chat_message: ChatMessage):
    # Step 1: Get the summary of the first question
    # first_question_summary = summarize_as_title(chat_message.question)
    # Step 2: Process this summary to create a chat name by selecting the first three words
    chat_name = " ".join(chat_message.question.split()[:3])

    return chat_name
