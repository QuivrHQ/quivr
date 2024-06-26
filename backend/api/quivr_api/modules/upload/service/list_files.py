from multiprocessing import get_logger

from quivr_api.models.settings import get_supabase_client
from supabase.client import Client

logger = get_logger()


def list_files_from_storage(path):
    supabase_client: Client = get_supabase_client()

    try:
        response = supabase_client.storage.from_("quivr").list(path)
        return response
    except Exception as e:
        logger.error(e)
