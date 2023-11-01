from uuid import UUID

from models import get_supabase_client


def get_shared_chat_by_id(shared_chat_id: UUID) -> str:
    supabase_client = get_supabase_client()
    response = (
        supabase_client.from_("shared_chats")
        .select("*")
        .filter("id", "eq", str(shared_chat_id))
        .execute()
    )

    shared_chat = response.data[0]
    chat_id = shared_chat["chat_id"]

    return chat_id
