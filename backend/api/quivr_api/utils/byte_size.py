def convert_bytes(bytes: int, precision=2):
    """Converts bytes into a human-friendly format."""
    abbreviations = ["B", "KB", "MB"]
    if bytes <= 0:
        return "0 B"
    size = bytes
    index = 0
    while size >= 1024 and index < len(abbreviations) - 1:
        size /= 1024
        index += 1
    return f"{size:.{precision}f} {abbreviations[index]}"
