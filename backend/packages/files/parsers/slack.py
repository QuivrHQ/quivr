from models import File
from packages.files.loaders.slack import SlackChatFileLoader

from .common import process_file


def process_slack(
    file: File,
    brain_id,
):
    return process_file(
        file=file,
        loader_class=SlackChatFileLoader,
        brain_id=brain_id,
    )
