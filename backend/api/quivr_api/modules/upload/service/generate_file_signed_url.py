from multiprocessing import get_logger

from quivr_api.modules.dependencies import get_supabase_client
from supabase.client import Client
import os

logger = get_logger()

SIGNED_URL_EXPIRATION_PERIOD_IN_SECONDS = 3600
EXTERNAL_SUPABASE_URL = os.getenv("EXTERNAL_SUPABASE_URL", None)
SUPABASE_URL = os.getenv("SUPABASE_URL", None)

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
        # Replace in the response the supabase url by the external supabase url in the object signedURL
        if EXTERNAL_SUPABASE_URL and SUPABASE_URL:
            response["signedURL"] = response["signedURL"].replace(SUPABASE_URL, EXTERNAL_SUPABASE_URL)
        return response
    except Exception as e:
        logger.error(e)
