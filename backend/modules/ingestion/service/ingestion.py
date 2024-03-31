from models.settings import get_supabase_client
from modules.ingestion.entity.ingestion import IngestionEntity
from modules.ingestion.repository.ingestion_interface import IngestionInterface


class Ingestion(IngestionInterface):
    def __init__(self):
        supabase_client = get_supabase_client()
        self.db = supabase_client

    def get_all_ingestions(self):
        response = self.db.from_("ingestions").select("*").execute()

        if response.data:
            return response.data

        return []

    def get_ingestion_by_id(self, ingestion_id) -> IngestionEntity:
        response = (
            self.db.from_("ingestions")
            .select("*")
            .filter("id", "eq", ingestion_id)
            .execute()
        )

        if response.data:
            return IngestionEntity(**response.data[0])

        return None
