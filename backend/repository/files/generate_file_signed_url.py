from multiprocessing import get_logger

from models import get_supabase_client
from supabase.client import Client

logger = get_logger()

SIGNED_URL_EXPIRATION_PERIOD_IN_SECONDS = 600


def generate_file_signed_url(path):
    supabase_client: Client = get_supabase_client()

    try:
        response = supabase_client.storage.from_("quivr").create_signed_url(
            path,
            SIGNED_URL_EXPIRATION_PERIOD_IN_SECONDS,
            options={
                "download": True,
                "transform": None,
            },
        )
        logger.info("RESPONSE SIGNED URL", response)
        return response
    except Exception as e:
        logger.error(e)
