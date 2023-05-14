from langchain.vectorstores import SupabaseVectorStore, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from abstract import VectorStoreInterface
from supabase import Client, create_client
import streamlit as st


supabase_url = st.secrets.supabase_url
supabase_key = st.secrets.supabase_service_key
pinecone_api_key = st.secrets.pinecone_api_key
pinecone_env = st.secrets.pinecone_env
pinecone_index = st.secrets.pinecone_index
openai_api_key = st.secrets.openai_api_key

class SupabaseVectorStore(VectorStoreInterface):
    def __init__(self, supabase, embeddings, table_name):
        self.supabase = supabase
        self.embeddings = embeddings
        self.table_name = table_name

    def select(self, *args, **kwargs):
        return self.supabase.table(self.table_name).select(*args, **kwargs).execute()

    def delete(self, *args, **kwargs):
        return self.supabase.table(self.table_name).delete().match(*args, **kwargs).execute()

def get_vectorestore():
    ## supabase: Client = create_client(supabase_url, supabase_key)
    #     embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    # vector_store = SupabaseVectorStore(
    #     supabase, embeddings, table_name="documents")
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)


    if pinecone_api_key :
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)
        index = pinecone.Index(pinecone_index)
        vectorstore = Pinecone(index, embeddings.embed_query, "text")
        return vectorstore
    else:
        supabase: Client = create_client(supabase_url, supabase_key)
        vector_store = SupabaseVectorStore(
            supabase, embeddings, table_name="documents")
        return vector_store