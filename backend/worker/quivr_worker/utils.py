import os
import uuid
from json import JSONEncoder
from pathlib import PosixPath
from typing import Tuple


def get_tmp_name(file_name: str) -> Tuple[str, str, str]:
    # Filepath is S3 based
    tmp_name = file_name.replace("/", "_")
    base_file_name = os.path.basename(file_name)
    _, file_extension = os.path.splitext(base_file_name)
    return tmp_name, base_file_name, file_extension


# TODO: This is a hack for making uuid work with supabase clients
# THIS is dangerous, I am patching json globally
def _patch_json():
    _default_encoder = JSONEncoder().default

    def _new_default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        if isinstance(obj, PosixPath):
            return str(obj)
        return _default_encoder(obj)

    JSONEncoder.default = _new_default  # type: ignore
