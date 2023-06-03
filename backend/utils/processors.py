import os

from fastapi import Depends, FastAPI, UploadFile
from models.users import User
from parsers.audio import process_audio
from parsers.common import file_already_exists
from parsers.csv import process_csv
from parsers.docx import process_docx
from parsers.epub import process_epub
from parsers.html import process_html
from parsers.markdown import process_markdown
from parsers.notebook import process_ipnyb
from parsers.odt import process_odt
from parsers.pdf import process_pdf
from parsers.powerpoint import process_powerpoint
from parsers.txt import process_txt
from supabase import Client

file_processors = {
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




async def filter_file(file: UploadFile, enable_summarization: bool, supabase_client: Client, user: User):
    if await file_already_exists(supabase_client, file, user):
        return {"message": f"🤔 {file.filename} already exists.", "type": "warning"}
    elif file.file._file.tell()  < 1:
        return {"message": f"❌ {file.filename} is empty.", "type": "error"}
    else:
        file_extension = os.path.splitext(file.filename)[-1].lower()  # Convert file extension to lowercase
        if file_extension in file_processors:
            await file_processors[file_extension](file, enable_summarization, user)
            return {"message": f"✅ {file.filename} has been uploaded.", "type": "success"}
        else:
            return {"message": f"❌ {file.filename} is not supported.", "type": "error"}

