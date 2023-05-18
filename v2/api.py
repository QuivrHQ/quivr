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


from common import file_already_exists
from txt import process_txt
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
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
    model: str
    question: str
    history: List[Tuple[str, str]]  # A list of tuples where each tuple is (speaker, text)

file_processors = {
    ".txt": process_txt,
}

async def filter_file(file: UploadFile, supabase, vector_store):
    if await file_already_exists(supabase, file):
        return f"😎 {file.filename} is already in the database."
    elif file.file._file.tell() < 1:
        return f"💨 {file.filename} is empty."
    else:
        file_extension = os.path.splitext(file.filename)[-1]
        if file_extension in file_processors:
            await file_processors[file_extension](vector_store, file, stats_db=None)
            return f"✅ {file.filename} "
        else:
            return f"❌ {file.filename} is not a valid file type."

@app.post("/upload")
async def upload_file(file: UploadFile):
    # Modify your code to work with FastAPI
    # Here we assume that you have some way to get `supabase`, `openai_key`, and `vector_store`
   
    print(f"Received file: {file.filename}")
   
    message = await filter_file(file, supabase, vector_store)
    
    return {"message": message}

@app.post("/chat/")
async def chat_endpoint(chat_message: ChatMessage):
    model = chat_message.model
    question = chat_message.question
    history = chat_message.history
    temperature = 0
    max_tokens = 100

    # Logic from your Streamlit app goes here. For example:
    qa = None
    if model.startswith("gpt"):
        qa = ConversationalRetrievalChain.from_llm(
            OpenAI(
                model_name=model, openai_api_key=openai_api_key, temperature=temperature, max_tokens=max_tokens), vector_store.as_retriever(), memory=memory, verbose=True)
    elif anthropic_api_key and model.startswith("claude"):
        qa = ConversationalRetrievalChain.from_llm(
            ChatAnthropic(
                model=model, anthropic_api_key=anthropic_api_key, temperature=temperature, max_tokens_to_sample=max_tokens), vector_store.as_retriever(), memory=memory, verbose=True, max_tokens_limit=102400)

    history.append(("user", question))
    model_response = qa({"question": question})
    history.append(("assistant", model_response["answer"]))

    return {"history": history}

@app.get("/")
async def root():
    return {"message": "Hello World"}