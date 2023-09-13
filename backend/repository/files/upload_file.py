from multiprocessing import get_logger

from httpx import Response
from models import get_supabase_client
from supabase.client import Client

logger = get_logger()


def upload_file_storage(file, file_identifier: str) -> Response:
    supabase_client: Client = get_supabase_client()
    # res = supabase_client.storage.create_bucket("quivr")
    response = None

    try:
        response = supabase_client.storage.from_("quivr").upload(file_identifier, file)
        return response
    except Exception as e:
        logger.error(e)
        return response
