from models.databases.supabase.shared_chats import CreateSharedChatProperties
from models import SharedChat, get_supabase_db


def create_shared_chat(shared_chat: CreateSharedChatProperties) -> SharedChat:
    supabase_db = get_supabase_db()

    return supabase_db.create_shared_chat(shared_chat)
