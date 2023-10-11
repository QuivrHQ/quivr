from typing import Optional
from uuid import UUID

from models import Chat, get_supabase_db
from models.databases.supabase.chats import QuestionAndAnswer


def add_question_and_answer(
    chat_id: UUID, question_and_answer: QuestionAndAnswer
) -> Optional[Chat]:
    supabase_db = get_supabase_db()

    return supabase_db.add_question_and_answer(chat_id, question_and_answer)
