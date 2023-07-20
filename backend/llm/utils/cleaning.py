import json
import logging

logger = logging.getLogger(__name__)


# -------------------
# Clean up LLM output
# -------------------
def sanitize_output(
    str_output: str
):
    # Let's sanitize the JSON
    res = str_output.replace("\n", '')

    # If the first character is "?", remove it. Ran into this issue for some reason.
    if res[0] == '?':
        res = res[1:]

    # check if response is valid json
    try:
        json.loads(res)
    except json.JSONDecodeError:
        raise ValueError(f'LLM response is not valid JSON: {res}')

    if 'message' not in res or 'tags' not in res or 'is_escalate' not in res:
        raise ValueError(f'LLM response is missing required fields: {res}')

    logger.debug(f'Output: {res}')
    return res


# ------------------
# Clean up LLM input
# ------------------
def sanitize_input(
    str_input: str
):
    # Escape single quotes that cause output JSON issues
    str_input = str_input.replace("'", "")

    logger.debug(f'Input: {str_input}')
    return str_input
