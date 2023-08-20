from uuid import UUID

from models import get_supabase_db
from routes.authorizations.types import RoleEnum


def create_brain_user(
    user_id: UUID, brain_id: UUID, rights: RoleEnum, is_default_brain: bool
) -> None:
    supabase_db = get_supabase_db()
    supabase_db.create_brain_user(
        user_id=user_id,
        brain_id=brain_id,
        rights=rights,
        default_brain=is_default_brain,
    ).data[0]
