import re


def normalize_to_env_variable_name(name: str) -> str:
    # Replace any character that is not a letter, digit, or underscore with an underscore
    env_variable_name = re.sub(r"[^A-Za-z0-9_]", "_", name).upper()

    # Check if the normalized name starts with a digit
    if env_variable_name[0].isdigit():
        raise ValueError(
            f"Invalid environment variable name '{env_variable_name}': Cannot start with a digit."
        )

    return env_variable_name
