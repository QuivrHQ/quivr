from logger import get_logger
from models.databases.supabase import (
    ApiBrainDefinitions,
    ApiKeyHandler,
    Brain,
    BrainSubscription,
    Chats,
    File,
    Knowledges,
    Notifications,
    Onboarding,
    Prompts,
    UserUsage,
    Vector,
)

logger = get_logger(__name__)


class SupabaseDB(
    Brain,
    UserUsage,
    File,
    BrainSubscription,
    ApiKeyHandler,
    Chats,
    Vector,
    Onboarding,
    Prompts,
    Notifications,
    Knowledges,
    ApiBrainDefinitions,
):
    def __init__(self, supabase_client):
        self.db = supabase_client
        Brain.__init__(self, supabase_client)
        UserUsage.__init__(self, supabase_client)
        File.__init__(self, supabase_client)
        BrainSubscription.__init__(self, supabase_client)
        ApiKeyHandler.__init__(self, supabase_client)
        Chats.__init__(self, supabase_client)
        Vector.__init__(self, supabase_client)
        Prompts.__init__(self, supabase_client)
        Notifications.__init__(self, supabase_client)
        Knowledges.__init__(self, supabase_client)
        Onboarding.__init__(self, supabase_client)
        ApiBrainDefinitions.__init__(self, supabase_client)
