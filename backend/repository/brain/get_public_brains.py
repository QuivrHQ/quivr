from models import get_supabase_db
from models.brain_entity import PublicBrain


def get_public_brains() -> list[PublicBrain]:
    supabase_db = get_supabase_db()
    return supabase_db.get_public_brains()
