from models import Chat, get_supabase_db


def get_chat_by_id(chat_id: str) -> Chat:
    supabase_db = get_supabase_db()

    response = supabase_db.get_chat_by_id(chat_id)
    return Chat(response.data[0])
