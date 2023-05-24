import os
import shutil
from configparser import ConfigParser
from tempfile import SpooledTemporaryFile
from typing import List, Tuple

import jwt
import pypandoc
from crawl.crawler import CrawlWebsite
from fastapi import Depends, FastAPI, File, HTTPException, UploadFile,Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from llm.qa import get_qa_llm
from llm.summarization import llm_evaluate_summaries
from logger import get_logger
from parsers.audio import process_audio
from parsers.common import file_already_exists
from parsers.csv import process_csv
from parsers.docx import process_docx
from parsers.epub import process_epub
from parsers.html import process_html
from parsers.markdown import process_markdown
from parsers.notebook import process_ipnyb
from parsers.pdf import process_pdf
from parsers.powerpoint import process_powerpoint
from parsers.txt import process_txt
from pydantic import BaseModel
from supabase import Client, create_client
from utils import ChatMessage, CommonsDep, similarity_search

logger = get_logger(__name__)


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Scheme for the Authorization header
token_auth_scheme = HTTPBearer()  # 👈 new code


def set_up():
    """Sets up configuration for the app"""

    env = os.getenv("ENV", ".config")

    if env == ".config":
        config = ConfigParser()
        config.read(".config")
        config = config["AUTH0"]
    else:
        config = {
            "DOMAIN": os.getenv("DOMAIN", "your.domain.com"),
            "API_AUDIENCE": os.getenv("API_AUDIENCE", "your.audience.com"),
            "ISSUER": os.getenv("ISSUER", "https://your.domain.com/"),
            "ALGORITHMS": os.getenv("ALGORITHMS", "RS256"),
        }
    return config
class VerifyToken():
    """Does all the token verification using PyJWT"""

    def __init__(self, token):
        self.token = token
        self.config = set_up()
        print(token)

        # This gets the JWKS from a given URL and does processing so you can
        # use any of the keys available
        jwks_url = f'https://{self.config["DOMAIN"]}/.well-known/jwks.json'
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        # This gets the 'kid' from the passed token
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}

        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms=self.config["ALGORITHMS"],
                audience=self.config["API_AUDIENCE"],
                issuer=self.config["ISSUER"],
            )
        except Exception as e:
            return {"status": "error", "message": str(e)}

        return payload

@app.on_event("startup")
async def startup_event():
    pypandoc.download_pandoc()


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
    ".epub": process_epub,
    ".ipynb": process_ipnyb,
}


async def filter_file(file: UploadFile, enable_summarization: bool, supabase_client: Client):
    if await file_already_exists(supabase_client, file):
        return {"message": f"🤔 {file.filename} already exists.", "type": "warning"}
    elif file.file._file.tell() < 1:
        return {"message": f"❌ {file.filename} is empty.", "type": "error"}
    else:
        file_extension = os.path.splitext(file.filename)[-1]
        if file_extension in file_processors:
            await file_processors[file_extension](file, enable_summarization)
            return {"message": f"✅ {file.filename} has been uploaded.", "type": "success"}
        else:
            return {"message": f"❌ {file.filename} is not supported.", "type": "error"}


@app.get("/private")
def private(response: Response, token: str = Depends(token_auth_scheme)):  # 👈 updated code
    """A valid access token is required to access this route"""
 
    result = VerifyToken(token.credentials).verify()  # 👈 updated code

    # 👇 new code
    if result.get("status"):
       response.status_code = status.HTTP_400_BAD_REQUEST
       return result
    # 👆 new code
 
    return result

@app.post("/upload")
async def upload_file(commons: CommonsDep, file: UploadFile, enable_summarization: bool = False):
    message = await filter_file(file, enable_summarization, commons['supabase'])
    return message


@app.post("/chat/")
async def chat_endpoint(commons: CommonsDep, chat_message: ChatMessage):
    history = chat_message.history
    qa = get_qa_llm(chat_message)
    history.append(("user", chat_message.question))

    if chat_message.use_summarization:
        # 1. get summaries from the vector store based on question
        summaries = similarity_search(
            chat_message.question, table='match_summaries')
        # 2. evaluate summaries against the question
        evaluations = llm_evaluate_summaries(
            chat_message.question, summaries, chat_message.model)
        # 3. pull in the top documents from summaries
        logger.info('Evaluations: %s', evaluations)
        if evaluations:
            reponse = commons['supabase'].from_('documents').select(
                '*').in_('id', values=[e['document_id'] for e in evaluations]).execute()
        # 4. use top docs as additional context
            additional_context = '---\nAdditional Context={}'.format(
                '---\n'.join(data['content'] for data in reponse.data)
            ) + '\n'
        model_response = qa(
            {"question": additional_context + chat_message.question})
    else:
        model_response = qa({"question": chat_message.question})
    history.append(("assistant", model_response["answer"]))

    return {"history": history}


@app.post("/crawl/")
async def crawl_endpoint(commons: CommonsDep, crawl_website: CrawlWebsite, enable_summarization: bool = False):
    file_path, file_name = crawl_website.process()

    # Create a SpooledTemporaryFile from the file_path
    spooled_file = SpooledTemporaryFile()
    with open(file_path, 'rb') as f:
        shutil.copyfileobj(f, spooled_file)

    # Pass the SpooledTemporaryFile to UploadFile
    file = UploadFile(file=spooled_file, filename=file_name)
    message = await filter_file(file, enable_summarization, commons['supabase'])
    return message


@app.get("/explore")
async def explore_endpoint(commons: CommonsDep):
    response = commons['supabase'].table("documents").select(
        "name:metadata->>file_name, size:metadata->>file_size", count="exact").execute()
    documents = response.data  # Access the data from the response
    # Convert each dictionary to a tuple of items, then to a set to remove duplicates, and then back to a dictionary
    unique_data = [dict(t) for t in set(tuple(d.items()) for d in documents)]
    # Sort the list of documents by size in decreasing order
    unique_data.sort(key=lambda x: int(x['size']), reverse=True)

    return {"documents": unique_data}


@app.delete("/explore/{file_name}")
async def delete_endpoint(commons: CommonsDep, file_name: str):
    # Cascade delete the summary from the database first, because it has a foreign key constraint
    commons['supabase'].table("summaries").delete().match(
        {"metadata->>file_name": file_name}).execute()
    commons['supabase'].table("documents").delete().match(
        {"metadata->>file_name": file_name}).execute()
    return {"message": f"{file_name} has been deleted."}


@app.get("/explore/{file_name}")
async def download_endpoint(commons: CommonsDep, file_name: str):
    response = commons['supabase'].table("documents").select(
        "metadata->>file_name, metadata->>file_size, metadata->>file_extension, metadata->>file_url").match({"metadata->>file_name": file_name}).execute()
    documents = response.data
    # Returns all documents with the same file name
    return {"documents": documents}


@app.get("/")
async def root():
    return {"message": "Hello World"}
