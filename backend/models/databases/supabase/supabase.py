from models.databases.supabase import (
    Brain,
    User,
    File,
    BrainSubscription,
    ApiKeyHandler,
    Chats,
    Vector,
)
from logger import get_logger


logger = get_logger(__name__)


class SupabaseDB(Brain, User, File, BrainSubscription, ApiKeyHandler, Chats, Vector):
    def __init__(self, supabase_client):
        self.db = supabase_client
