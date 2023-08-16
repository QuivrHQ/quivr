from models.databases.supabase.brains import CreateBrainProperties
from models import BrainEntity, get_supabase_db


def create_brain(brain: CreateBrainProperties) -> BrainEntity:
    supabase_db = get_supabase_db()

    return supabase_db.create_brain(brain)
