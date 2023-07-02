from models.brains import Brain
from models.files import File
from models.settings import CommonsDep
from parsers.audio import process_audio  # pyright: ignore reportPrivateUsage=none
from parsers.csv import process_csv  # pyright: ignore reportPrivateUsage=none
from parsers.docx import process_docx  # pyright: ignore reportPrivateUsage=none
from parsers.epub import process_epub  # pyright: ignore reportPrivateUsage=none
from parsers.html import process_html  # pyright: ignore reportPrivateUsage=none
from parsers.markdown import process_markdown  # pyright: ignore reportPrivateUsage=none
from parsers.notebook import process_ipnyb  # pyright: ignore reportPrivateUsage=none
from parsers.odt import process_odt  # pyright: ignore reportPrivateUsage=none
from parsers.pdf import process_pdf  # pyright: ignore reportPrivateUsage=none
from parsers.powerpoint import (
    process_powerpoint,  # pyright: ignore reportPrivateUsage=none
)
from parsers.txt import process_txt  # pyright: ignore reportPrivateUsage=none

file_processors = {  # pyright: ignore reportPrivateUsage=none
    ".txt": process_txt,
    ".csv": process_csv,
    ".md": process_markdown,
    ".markdown": process_markdown,
    ".m4a": process_audio,
    ".mp3": process_audio,
    ".webm": process_audio,
    ".mp4": process_audio,
    ".mpga": process_audio,
    ".wav": process_audio,
    ".mpeg": process_audio,
    ".pdf": process_pdf,
    ".html": process_html,
    ".pptx": process_powerpoint,
    ".docx": process_docx,
    ".odt": process_odt,
    ".epub": process_epub,
    ".ipynb": process_ipnyb,
}


def create_response(message, type):  # pyright: ignore reportPrivateUsage=none
    return {"message": message, "type": type}  # pyright: ignore reportPrivateUsage=none


async def filter_file( # pyright: ignore reportPrivateUsage=none
    commons: CommonsDep,
    file: File,
    enable_summarization: bool,
    brain_id,  # pyright: ignore reportPrivateUsage=none
    openai_api_key,  # pyright: ignore reportPrivateUsage=none
):
    await file.compute_file_sha1()

    print("file sha1", file.file_sha1)
    file_exists = file.file_already_exists()
    file_exists_in_brain = (
        file.file_already_exists_in_brain(  # pyright: ignore reportPrivateUsage=none
            brain_id,  # pyright: ignore reportPrivateUsage=none
        )
    )

    if file_exists_in_brain:
        return create_response(
            f"🤔 {file.file.filename} already exists in brain {brain_id}." # pyright: ignore reportPrivateUsage=none,
            "warning", 
        )
    elif file.file_is_empty():
        return create_response(
            f"❌ {file.file.filename} is empty."  # pyright: ignore reportPrivateUsage=none,
            "error",
        )
    elif file_exists:
        file.link_file_to_brain(
            brain=Brain(id=brain_id)  # pyright: ignore reportPrivateUsage=none
        )  # pyright: ignore reportPrivateUsage=none
        return create_response(
            f"✅ {file.file.filename} has been uploaded to brain {brain_id}."  # pyright: ignore reportPrivateUsage=none,
            "success",
        )

    if file.file_extension in file_processors:
        try:
            await file_processors[file.file_extension]( # pyright: ignore reportPrivateUsage=none
                commons,
                file,
                enable_summarization,
                brain_id # pyright: ignore reportPrivateUsage=none,
                openai_api_key,  # pyright: ignore reportPrivateUsage=none
            )
            return create_response(
                f"✅ {file.file.filename} has been uploaded to brain {brain_id}." # pyright: ignore reportPrivateUsage=none,
                "success",
            )
        except Exception as e:
            # Add more specific exceptions as needed.
            print(f"Error processing file: {e}")
            return create_response(
                f"⚠️ An error occurred while processing {file.file.filename}.", "error" # pyright: ignore reportPrivateUsage=none,
            )

    return create_response(f"❌ {file.file.filename} is not supported.", "error") # pyright: ignore reportPrivateUsage=none
