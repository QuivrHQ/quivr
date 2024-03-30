from models.settings import get_supabase_client
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
