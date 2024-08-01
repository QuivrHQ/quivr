import hashlib
from io import BytesIO

from fastapi import UploadFile


def get_file_size(file: UploadFile):
    if isinstance(file.file, BytesIO):
        # If the file object is a BytesIO object, get the size of the bytes data
        file_size = len(file.file.getvalue())
        return file_size
    # move the cursor to the end of the file
    file.file._file.seek(0, 2)  # pyright: ignore reportPrivateUsage=none
    file_size = (
        file.file._file.tell()  # pyright: ignore reportPrivateUsage=none
    )  # Getting the size of the file
    # move the cursor back to the beginning of the file
    file.file.seek(0)

    return file_size


def compute_sha1_from_file(file_path):
    with open(file_path, "rb") as file:
        bytes = file.read()
        readable_hash = compute_sha1_from_content(bytes)
    return readable_hash


def compute_sha1_from_content(content):
    readable_hash = hashlib.sha1(content).hexdigest()
    return readable_hash
