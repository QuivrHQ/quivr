import uuid
from json import JSONEncoder
from pathlib import PosixPath


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
