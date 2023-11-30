from logger import get_logger
from models.databases.supabase import (
    ApiBrainDefinitions,
    BrainSubscription,
    Chats,
    File,
    UserUsage,
    Vector,
)

logger = get_logger(__name__)


class SupabaseDB(
    UserUsage,
    File,
    BrainSubscription,
    Chats,
    Vector,
    ApiBrainDefinitions,
):
    def __init__(self, supabase_client):
        self.db = supabase_client
        UserUsage.__init__(self, supabase_client)
        File.__init__(self, supabase_client)
        BrainSubscription.__init__(self, supabase_client)
        Chats.__init__(self, supabase_client)
        Vector.__init__(self, supabase_client)
        ApiBrainDefinitions.__init__(self, supabase_client)
