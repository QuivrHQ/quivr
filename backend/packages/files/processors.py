from modules.brain.service.brain_service import BrainService

from .parsers.audio import process_audio
from .parsers.code_python import process_python
from .parsers.csv import process_csv
from .parsers.docx import process_docx
from .parsers.epub import process_epub
from .parsers.html import process_html
from .parsers.markdown import process_markdown
from .parsers.notebook import process_ipnyb
from .parsers.odt import process_odt
from .parsers.pdf import process_pdf
from .parsers.powerpoint import process_powerpoint
from .parsers.telegram import process_telegram
from .parsers.txt import process_txt
from .parsers.xlsx import process_xlsx
from .parsers.bibtex import process_bibtex

file_processors = {
    ".txt": process_txt,
    ".csv": process_csv,
    ".md": process_markdown,
    ".markdown": process_markdown,
    ".telegram": process_telegram,
    ".m4a": process_audio,
    ".mp3": process_audio,
    ".webm": process_audio,
    ".mp4": process_audio,
    ".mpga": process_audio,
    ".wav": process_audio,
    ".mpeg": process_audio,
    ".pdf": process_pdf,
    ".html": process_html,
    ".bib": process_bibtex,
    ".pptx": process_powerpoint,
    ".docx": process_docx,
    ".odt": process_odt,
    ".xlsx": process_xlsx,
    ".xls": process_xlsx,
    ".epub": process_epub,
    ".ipynb": process_ipnyb,
    ".py": process_python,
}


def create_response(message, type):
    return {"message": message, "type": type}


brain_service = BrainService()


# TODO: Move filter_file to a file service to avoid circular imports from models/files.py for File class
async def filter_file(
    file,
    brain_id,
    original_file_name=None,
):
    await file.compute_file_sha1()

    file_exists = file.file_already_exists()
    file_exists_in_brain = file.file_already_exists_in_brain(brain_id)
    using_file_name = original_file_name or file.file.filename if file.file else ""

    brain = brain_service.get_brain_by_id(brain_id)
    if brain is None:
        raise Exception("It seems like you're uploading knowledge to an unknown brain.")

    if file_exists_in_brain:
        return create_response(
            f"🤔 {using_file_name} already exists in brain {brain.name}.",  # pyright: ignore reportPrivateUsage=none
            "warning",
        )
    elif file.file_is_empty():
        return create_response(
            f"❌ {original_file_name} is empty.",  # pyright: ignore reportPrivateUsage=none
            "error",  # pyright: ignore reportPrivateUsage=none
        )
    elif file_exists:
        file.link_file_to_brain(brain_id)
        return create_response(
            f"✅ {using_file_name} has been uploaded to brain {brain.name}.",  # pyright: ignore reportPrivateUsage=none
            "success",
        )

    if file.file_extension in file_processors:
        try:
            result = await file_processors[file.file_extension](
                file=file,
                brain_id=brain_id,
                original_file_name=original_file_name,
            )
            if result is None or result == 0:
                return create_response(
                    f"？ {using_file_name} has been uploaded to brain. There might have been an error while reading it, please make sure the file is not illformed or just an image",  # pyright: ignore reportPrivateUsage=none
                    "warning",
                )
            return create_response(
                f"✅ {using_file_name} has been uploaded to brain {brain.name} in {result} chunks",  # pyright: ignore reportPrivateUsage=none
                "success",
            )
        except Exception as e:
            # Add more specific exceptions as needed.
            print(f"Error processing file: {e}")
            return create_response(
                f"⚠️ An error occurred while processing {using_file_name}.",  # pyright: ignore reportPrivateUsage=none
                "error",
            )

    return create_response(
        f"❌ {using_file_name} is not supported.",  # pyright: ignore reportPrivateUsage=none
        "error",
    )
