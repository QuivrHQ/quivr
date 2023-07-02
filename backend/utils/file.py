import hashlib

from fastapi import UploadFile


def convert_bytes(bytes, precision=2):  # pyright: ignore reportPrivateUsage=none
    """Converts bytes into a human-friendly format."""
    abbreviations = ["B", "KB", "MB"]
    if bytes <= 0:
        return "0 B"
    size = bytes  # pyright: ignore reportPrivateUsage=none
    index = 0
    while size >= 1024 and index < len(abbreviations) - 1:
        size /= 1024  # pyright: ignore reportPrivateUsage=none
        index += 1
    return f"{size:.{precision}f} {abbreviations[index]}"


def get_file_size(file: UploadFile):  # pyright: ignore reportPrivateUsage=none
    # move the cursor to the end of the file
    file.file._file.seek(0, 2)  # pyright: ignore reportPrivateUsage=none
    file_size = (  # pyright: ignore reportPrivateUsage=none
        file.file._file.tell()  # pyright: ignore reportPrivateUsage=none
    )  # Getting the size of the file # pyright: ignore reportPrivateUsage=none
    # move the cursor back to the beginning of the file
    file.file.seek(0)

    return file_size  # pyright: ignore reportPrivateUsage=none


def compute_sha1_from_file(file_path):  # pyright: ignore reportPrivateUsage=none
    with open(file_path, "rb") as file:  # pyright: ignore reportPrivateUsage=none
        bytes = file.read()
        readable_hash = compute_sha1_from_content(bytes)
    return readable_hash


def compute_sha1_from_content(content):  # pyright: ignore reportPrivateUsage=none
    readable_hash = hashlib.sha1(
        content  # pyright: ignore reportPrivateUsage=none
    ).hexdigest()  # pyright: ignore reportPrivateUsage=none
    return readable_hash
