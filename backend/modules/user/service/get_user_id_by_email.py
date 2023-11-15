from uuid import UUID

from modules.user.repository import get_user_id_by_user_email


def get_user_id_by_email(email: str) -> UUID | None:
    return get_user_id_by_user_email(email)
