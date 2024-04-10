from models.settings import get_supabase_client
from modules.assistant.entity.assistant import AssistantEntity
from modules.assistant.repository.assistant_interface import AssistantInterface


class Assistant(AssistantInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client

    def get_all_assistants(self):
        response = self.db.from_("assistants").select("*").execute()

        if response.data:
            return response.data

        return []

    def get_assistant_by_id(self, ingestion_id) -> AssistantEntity:
        response = (
            self.db.from_("assistants")
            .select("*")
            .filter("id", "eq", ingestion_id)
            .execute()
        )

        if response.data:
            return AssistantEntity(**response.data[0])

        return None
