from models.chat import Chat
from models.settings import get_supabase_client


def get_chat_by_id(chat_id: str) -> Chat:
    supabase_client = get_supabase_client()

    response = (
        supabase_client.from_("chats")
        .select("*")
        .filter("chat_id", "eq", chat_id)
        .execute()
    )
    return Chat(response.data[0])
