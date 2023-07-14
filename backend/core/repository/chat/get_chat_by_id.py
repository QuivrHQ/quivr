from models.chat import Chat
from models.settings import common_dependencies


def get_chat_by_id(chat_id: str) -> Chat:
    commons = common_dependencies()

    response = (
        commons["supabase"]
        .from_("chats")
        .select("*")
        .filter("chat_id", "eq", chat_id)
        .execute()
    )
    return Chat(response.data[0])
