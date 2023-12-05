import os
from dotenv import load_dotenv

load_dotenv("./backend/.env")

print("CELERY_BROKER_URL:", os.environ.get("CELERY_BROKER_URL"))

from celery_worker import process_file_and_notify

test_file_name = "8cd2e1fd-8aa4-43d5-bd33-a24bfbdfb5ad/dgnb-kriterienkatalog-gebaeude-neubau-version-2023-auflage-2.pdf"
test_file_original_name = (
    "dgnb-kriterienkatalog-gebaeude-neubau-version-2023-auflage-2.pdf"
)
enable_summarization = False
brain_id = "8cd2e1fd-8aa4-43d5-bd33-a24bfbdfb5ad"
openai_api_key = ""

# file_sha1 = 22b77dd61e05a6d3b64643be62b8edd71ca66cae

process_file_and_notify(
    file_name=test_file_name,
    file_original_name=test_file_original_name,
    enable_summarization=enable_summarization,
    brain_id=brain_id,
    openai_api_key=openai_api_key,
)
