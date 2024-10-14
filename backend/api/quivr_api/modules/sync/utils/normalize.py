import os
import re
import unicodedata

from quivr_api.logger import get_logger

logger = get_logger(__name__)


def remove_special_characters(input):
    try:
        normalized_string = unicodedata.normalize("NFD", input)
        normalized_string = re.sub(r"[^\w\s.]", "", normalized_string)
        logger.info(f"Input: {input}, Normalized: {normalized_string}")
        return normalized_string
    except Exception as e:
        logger.error(f"Error removing special characters: {e}")
        return input


def sanitize_filename(filename: str) -> str:
    """
    Sanitize the filename to make it usable.

    Args:
        filename (str): The original filename.

    Returns:
        str: The sanitized filename.

    This function:
    1. Removes or replaces invalid characters
    2. Handles double extensions
    3. Ensures the filename is not empty
    4. Truncates long filenames
    """
    valid_chars = re.sub(r"[^\w\-_\. ]", "", filename)

    name, ext = os.path.splitext(valid_chars)

    name = name.replace(".", "_")

    if not name:
        name = "unnamed"
    max_length = 255 - len(ext)
    if len(name) > max_length:
        name = name[:max_length]
    sanitized_filename = f"{name}{ext}"

    return sanitized_filename
