from quivr_core.files.file import FileExtension


def parse_file_extension(file_name: str) -> FileExtension | str:
    if file_name.startswith(".") and file_name.count(".") == 1:
        return ""
    if "." not in file_name or file_name.endswith("."):
        return ""

    return FileExtension(f".{file_name.split('.')[-1]}")
