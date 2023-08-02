from logger import get_logger
from models.databases.supabase import (
    ApiKeyHandler,
    Brain,
    BrainSubscription,
    Chats,
    File,
    Prompts,
    User,
    Vector,
)

logger = get_logger(__name__)


class SupabaseDB(
    Brain, User, File, BrainSubscription, ApiKeyHandler, Chats, Vector, Prompts
):
    def __init__(self, supabase_client):
        self.db = supabase_client
        Brain.__init__(self, supabase_client)
        User.__init__(self, supabase_client)
        File.__init__(self, supabase_client)
        BrainSubscription.__init__(self, supabase_client)
        ApiKeyHandler.__init__(self, supabase_client)
        Chats.__init__(self, supabase_client)
        Vector.__init__(self, supabase_client)
        Prompts.__init__(self, supabase_client)
