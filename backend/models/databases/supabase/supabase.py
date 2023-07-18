from models.databases.supabase.brains import Brain
from logger import get_logger


logger = get_logger(__name__)


class SupabaseDB(Brain):
    def __init__(self, supabase_client):
        self.db = supabase_client
