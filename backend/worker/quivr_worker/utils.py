import os
from typing import Tuple


def get_tmp_name(file_name: str) -> Tuple[str, str, str]:
    # Filepath is S3 based
    tmp_name = file_name.replace("/", "_")
    base_file_name = os.path.basename(file_name)
    _, file_extension = os.path.splitext(base_file_name)
    return tmp_name, base_file_name, file_extension
