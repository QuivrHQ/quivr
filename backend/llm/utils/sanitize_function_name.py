import re


def sanitize_function_name(string):
    sanitized_string = re.sub(r"[^a-zA-Z0-9_-]", "", string)

    return sanitized_string
