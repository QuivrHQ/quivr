import os
from typing import Annotated, List, Tuple

from fastapi import Depends, UploadFile
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import SupabaseVectorStore
from llm.summarization import llm_summerize
from logger import get_logger
from pydantic import BaseModel

from supabase import Client, create_client

logger = get_logger(__name__)


openai_api_key = os.environ.get("OPENAI_API_KEY")
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
supabase_client: Client = create_client(supabase_url, supabase_key)
documents_vector_store = SupabaseVectorStore(
    supabase_client, embeddings, table_name="vectors")
summaries_vector_store = SupabaseVectorStore(
    supabase_client, embeddings, table_name="summaries")





def common_dependencies():
    return {
        "supabase": supabase_client,
        "embeddings": embeddings,
        "documents_vector_store": documents_vector_store,
        "summaries_vector_store": summaries_vector_store
    }


CommonsDep = Annotated[dict, Depends(common_dependencies)]




def create_summary(document_id, content, metadata):
    logger.info(f"Summarizing document {content[:100]}")
    summary = llm_summerize(content)
    logger.info(f"Summary: {summary}")
    metadata['document_id'] = document_id
    summary_doc_with_metadata = Document(
        page_content=summary, metadata=metadata)
    sids = summaries_vector_store.add_documents(
        [summary_doc_with_metadata])
    if sids and len(sids) > 0:
        supabase_client.table("summaries").update(
            {"document_id": document_id}).match({"id": sids[0]}).execute()

def create_vector(user_id,doc):
    logger.info(f"Creating vector for document")
    logger.info(f"Document: {doc}")
    try:
        sids = documents_vector_store.add_documents(
            [doc])
        if sids and len(sids) > 0:
            supabase_client.table("vectors").update(
                {"user_id": user_id}).match({"id": sids[0]}).execute()
    except Exception as e:
        logger.error(f"Error creating vector for document {e}")

def create_user(email, date):
    logger.info(f"New user entry in db document for user {email}")
    return(supabase_client.table("users").insert(
        {"email": email, "date": date, "requests_count": 1}).execute())

def update_user_request_count(email, date, requests_count):
    logger.info(f"User {email} request count updated to {requests_count}")
    supabase_client.table("users").update(
        { "requests_count": requests_count}).match({"email": email, "date": date}).execute()

def create_chat(user_id):
    logger.info(f"New chat entry in chats table for user {user_id}")

    # Insert a new row into the chats table
    new_chat = {
        "user_id": user_id,
        "history": {}  # Empty chat to start
    }
    insert_response = supabase_client.table('chats').insert(new_chat).execute()
    return(insert_response)

def update_chat(chat_id, history):
    supabase_client.table("chats").update(
        { "history": history}).match({"chat_id": chat_id}).execute()
    logger.info(f"Chat {chat_id} updated")
    

def create_embedding(content):
    return embeddings.embed_query(content)



def similarity_search(query, table='match_summaries', top_k=5, threshold=0.5):
    query_embedding = create_embedding(query)
    summaries = supabase_client.rpc(
        table, {'query_embedding': query_embedding,
                'match_count': top_k, 'match_threshold': threshold}
    ).execute()
    return summaries.data



