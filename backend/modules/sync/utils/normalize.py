import unicodedata
import re
from logger import get_logger

logger = get_logger(__name__)

def remove_special_characters(input):
    try:
        normalized_string = unicodedata.normalize('NFD', input)
        normalized_string = re.sub(r'[^\w\s.]', '', normalized_string)
        logger.info(f"Input: {input}, Normalized: {normalized_string}")
        return normalized_string
    except Exception as e:
        logger.error(f"Error removing special characters: {e}")
        return input