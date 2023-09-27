from multiprocessing import get_logger

from models import get_supabase_client
from supabase.client import Client

logger = get_logger()


def delete_file_from_storage(file_identifier: str):
    supabase_client: Client = get_supabase_client()

    try:
        response = supabase_client.storage.from_("quivr").remove([file_identifier])
        return response
    except Exception as e:
        logger.error(e)
        raise e
