from models import File
from packages.files.loaders.telegram import TelegramChatFileLoader

from .common import process_file


def process_telegram(
    file: File,
    brain_id,
):
    return process_file(
        file=file,
        loader_class=TelegramChatFileLoader,
        brain_id=brain_id,
    )
