from fastapi import FastAPI, UploadFile, File, HTTPException
import os
from pydantic import BaseModel
from typing import List, Tuple
from supabase import create_client, Client
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import SupabaseVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from fastapi.openapi.utils import get_openapi
from tempfile import SpooledTemporaryFile
import shutil


from parsers.common import file_already_exists
from parsers.txt import process_txt
from parsers.csv import process_csv
from parsers.docx import process_docx
from parsers.pdf import process_pdf
from parsers.markdown import process_markdown
from parsers.powerpoint import process_powerpoint
from parsers.html import process_html
from parsers.audio import process_audio
from crawl.crawler import CrawlWebsite


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
openai_api_key = os.environ.get("OPENAI_API_KEY")
anthropic_api_key = ""
supabase: Client = create_client(supabase_url, supabase_key)
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vector_store = SupabaseVectorStore(
    supabase, embeddings, table_name="documents")
memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)


class ChatMessage(BaseModel):
    model: str = "gpt-3.5-turbo"
    question: str
    history: List[Tuple[str, str]]  # A list of tuples where each tuple is (speaker, text)
    temperature: float = 0.0
    max_tokens: int = 256






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
    ".docx": process_docx
}

async def filter_file(file: UploadFile, supabase, vector_store, stats_db):
    if await file_already_exists(supabase, file):
        return {"message": f"🤔 {file.filename} already exists.", "type": "warning"}
    elif file.file._file.tell() < 1:
        return {"message": f"❌ {file.filename} is empty.", "type": "error"}
    else:
        file_extension = os.path.splitext(file.filename)[-1]
        if file_extension in file_processors:
            await file_processors[file_extension](vector_store, file, stats_db=None)
            return {"message": f"✅ {file.filename} has been uploaded.", "type": "success"}
        else:
            return {"message": f"❌ {file.filename} is not supported.", "type": "error"}

@app.post("/upload")
async def upload_file(file: UploadFile):
    message = await filter_file(file, supabase, vector_store, stats_db=None)
    return message

@app.post("/chat/")
async def chat_endpoint(chat_message: ChatMessage):
    history = chat_message.history
    # Logic from your Streamlit app goes here. For example:
    qa = None
    if chat_message.model.startswith("gpt"):
        qa = ConversationalRetrievalChain.from_llm(
            OpenAI(
                model_name=chat_message.model, openai_api_key=openai_api_key, temperature=chat_message.temperature, max_tokens=chat_message.max_tokens), vector_store.as_retriever(), memory=memory, verbose=True)
    elif anthropic_api_key and model.startswith("claude"):
        qa = ConversationalRetrievalChain.from_llm(
            ChatAnthropic(
                model=model, anthropic_api_key=anthropic_api_key, temperature=temperature, max_tokens_to_sample=max_tokens), vector_store.as_retriever(), memory=memory, verbose=True, max_tokens_limit=102400)

    history.append(("user", chat_message.question))
    model_response = qa({"question": chat_message.question})
    history.append(("assistant", model_response["answer"]))

    return {"history": history}

@app.post("/crawl/")
async def crawl_endpoint(crawl_website: CrawlWebsite):
    
    file_path, file_name = crawl_website.process()

    # Create a SpooledTemporaryFile from the file_path
    spooled_file = SpooledTemporaryFile()
    with open(file_path, 'rb') as f:
        shutil.copyfileobj(f, spooled_file)

    # Pass the SpooledTemporaryFile to UploadFile
    file = UploadFile(file=spooled_file, filename=file_name)
    message = await filter_file(file, supabase, vector_store)
    print(message)
    return {"message": message}

@app.get("/explore")
async def explore_endpoint():
    response = supabase.table("documents").select("name:metadata->>file_name, size:metadata->>file_size", count="exact").execute()
    documents = response.data  # Access the data from the response
    # Convert each dictionary to a tuple of items, then to a set to remove duplicates, and then back to a dictionary
    unique_data = [dict(t) for t in set(tuple(d.items()) for d in documents)]
    # Sort the list of documents by size in decreasing order
    unique_data.sort(key=lambda x: int(x['size']), reverse=True)

    return {"documents": unique_data}

@app.delete("/explore/{file_name}")
async def delete_endpoint(file_name: str):
    response = supabase.table("documents").delete().match({"metadata->>file_name": file_name}).execute()
    return {"message": f"{file_name} has been deleted."}

@app.get("/explore/{file_name}")
async def download_endpoint(file_name: str):
    response = supabase.table("documents").select("metadata->>file_name, metadata->>file_size, metadata->>file_extension, metadata->>file_url").match({"metadata->>file_name": file_name}).execute()
    documents = response.data
    ### Returns all documents with the same file name
    return {"documents": documents}



@app.get("/")
async def root():
    return {"message": "Hello World"}


