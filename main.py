import os
import tempfile

import streamlit as st
from sidebar import sidebar
from files import file_uploader
from question import chat_with_doc
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from supabase import Client, create_client



# supabase_url = "https://fqgpcifsfmamprzldyiv.supabase.co"
supabase_url = st.secrets.supabase_url
supabase_key = st.secrets.supabase_key
openai_api_key = st.secrets.openai_api_key
supabase: Client = create_client(supabase_url, supabase_key)

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vector_store = SupabaseVectorStore(supabase, embeddings, table_name="documents")




st.title("🧠 Second Brain 🧠")
st.markdown("Store your knowledge in a vector store and query it with OpenAI's GPT-3/4.")
st.markdown("---\n\n")



sidebar(supabase)
file_uploader(supabase,openai_api_key, vector_store)
st.markdown("---\n\n")
chat_with_doc(openai_api_key, vector_store)
