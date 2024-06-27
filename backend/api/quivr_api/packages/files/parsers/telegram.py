from quivr_api.models.files import File
from quivr_api.packages.files.loaders.telegram import TelegramChatFileLoader

from .common import process_file


def process_telegram(
    file: File, brain_id, original_file_name, integration=None, integration_link=None
):
    return process_file(
        file=file,
        loader_class=TelegramChatFileLoader,
        brain_id=brain_id,
        original_file_name=original_file_name,
        integration=integration,
        integration_link=integration_link,
    )
