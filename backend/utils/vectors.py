import os
from typing import Annotated, List, Tuple

from auth.auth_bearer import JWTBearer
from fastapi import Depends, UploadFile
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import SupabaseVectorStore
from llm.qa import get_qa_llm
from llm.summarization import llm_evaluate_summaries, llm_summerize
from logger import get_logger
from models.chats import ChatMessage
from models.users import User
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

def create_vector(user_id,doc, user_openai_api_key=None):
    logger.info(f"Creating vector for document")
    logger.info(f"Document: {doc}")
    if user_openai_api_key:
        documents_vector_store._embedding = embeddings_request = OpenAIEmbeddings(openai_api_key=user_openai_api_key)
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

def create_chat(user_id, history, chat_name):
    # Chat is created upon the user's first question asked
    logger.info(f"New chat entry in chats table for user {user_id}")
    
    # Insert a new row into the chats table
    new_chat = {
        "user_id": user_id,
        "history": history, # Empty chat to start
        "chat_name": chat_name
    }
    insert_response = supabase_client.table('chats').insert(new_chat).execute()
    logger.info(f"Insert response {insert_response.data}")

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





def fetch_user_id_from_credentials(commons: CommonsDep,date,credentials):
    user = User(email=credentials.get('email', 'none'))

    # Fetch the user's UUID based on their email
    response = commons['supabase'].from_('users').select('user_id').filter("email", "eq", user.email).execute()

    userItem = next(iter(response.data or []), {})

    if userItem == {}: 
        create_user_response = create_user(email= user.email, date=date)
        user_id = create_user_response.data[0]['user_id']

    else: 
        user_id = userItem['user_id']

    # if not(user_id):
    #     throw error
    return user_id

def get_chat_name_from_first_question(chat_message: ChatMessage):
    # Step 1: Get the summary of the first question        
    # first_question_summary = summerize_as_title(chat_message.question)
    # Step 2: Process this summary to create a chat name by selecting the first three words
    chat_name = ' '.join(chat_message.question.split()[:3])
    print('chat_name')
    return chat_name
   
def get_answer(commons: CommonsDep,  chat_message: ChatMessage, email: str, user_openai_api_key:str):
    qa = get_qa_llm(chat_message, email, user_openai_api_key)


    if chat_message.use_summarization:
        # 1. get summaries from the vector store based on question
        summaries = similarity_search(
            chat_message.question, table='match_summaries')
        # 2. evaluate summaries against the question
        evaluations = llm_evaluate_summaries(
            chat_message.question, summaries, chat_message.model)
        # 3. pull in the top documents from summaries
        # logger.info('Evaluations: %s', evaluations)
        if evaluations:
            reponse = commons['supabase'].from_('vectors').select(
                '*').in_('id', values=[e['document_id'] for e in evaluations]).execute()
        # 4. use top docs as additional context
            additional_context = '---\nAdditional Context={}'.format(
                '---\n'.join(data['content'] for data in reponse.data)
            ) + '\n'
        model_response = qa(
            {"question": additional_context + chat_message.question})
    else:
        model_response = qa({"question": chat_message.question})

    answer = model_response['answer']   

    # append sources (file_name) to answer
    if "source_documents" in answer:
        # logger.debug('Source Documents: %s', answer["source_documents"])
        sources = [
            doc.metadata["file_name"] for doc in answer["source_documents"]
            if "file_name" in doc.metadata]
        # logger.debug('Sources: %s', sources)
        if sources:
            files = dict.fromkeys(sources)
            # # shall provide file links until pages available
            # files = [f"[{f}](/explore/{f})" for f in files]
            answer = answer + "\n\nRef: " + "; ".join(files)

    return answer
   

