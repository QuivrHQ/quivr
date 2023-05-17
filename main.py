# main.py
import os
import tempfile

import streamlit as st
from files import file_uploader, url_uploader
from question import chat_with_doc
from brain import brain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from supabase import Client, create_client
from explorer import view_document
from stats import get_usage_today

supabase_url = st.secrets.supabase_url
supabase_key = st.secrets.supabase_service_key
openai_api_key = st.secrets.openai_api_key
anthropic_api_key = st.secrets.anthropic_api_key
supabase: Client = create_client(supabase_url, supabase_key)
self_hosted = st.secrets.self_hosted



embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vector_store = SupabaseVectorStore(
    supabase, embeddings, table_name="documents")
models = ["gpt-3.5-turbo", "gpt-4"]
if anthropic_api_key:
    models += ["claude-v1", "claude-v1.3",
               "claude-instant-v1-100k", "claude-instant-v1.1-100k"]

# Set the theme
st.set_page_config(
    page_title="Quivr",
    layout="wide",
    initial_sidebar_state="expanded",
)


    

st.title("🧠 Quivr - Your second brain 🧠")
st.markdown("Store your knowledge in a vector store and query it with OpenAI's GPT-3/4.")
st.markdown("---\n\n")

st.session_state["overused"] = False
if self_hosted == "false":
    usage = get_usage_today(supabase)
    st.write(f"Usage today: {usage} tokens out of {st.secrets.usage_limit}")
    st.write("---")
    if usage > st.secrets.usage_limit:
        
        st.error(
            f"You have used {usage} tokens today, which is more than your daily limit of {st.secrets.usage_limit} tokens. Please come back in a few or self host.")
        st.session_state["overused"] = True



# Initialize session state variables
if 'model' not in st.session_state:
    st.session_state['model'] = "gpt-3.5-turbo"
if 'temperature' not in st.session_state:
    st.session_state['temperature'] = 0.0
if 'chunk_size' not in st.session_state:
    st.session_state['chunk_size'] = 500
if 'chunk_overlap' not in st.session_state:
    st.session_state['chunk_overlap'] = 0
if 'max_tokens' not in st.session_state:
    st.session_state['max_tokens'] = 256

# Create a radio button for user to choose between adding knowledge or asking a question
user_choice = st.radio(
    "Choose an action", ('Add Knowledge', 'Chat with your Brain', 'Forget', "Explore"))

st.markdown("---\n\n")

if user_choice == 'Add Knowledge':
    # Display chunk size and overlap selection only when adding knowledge
    st.sidebar.title("Configuration")
    st.sidebar.markdown(
        "Choose your chunk size and overlap for adding knowledge.")
    st.session_state['chunk_size'] = st.sidebar.slider(
        "Select Chunk Size", 100, 1000, st.session_state['chunk_size'], 50)
    st.session_state['chunk_overlap'] = st.sidebar.slider(
        "Select Chunk Overlap", 0, 100, st.session_state['chunk_overlap'], 10)
    
    # Create two columns for the file uploader and URL uploader
    col1, col2 = st.columns(2)
    
    with col1:
        file_uploader(supabase, openai_api_key, vector_store)
    with col2:
        url_uploader(supabase, openai_api_key, vector_store)
elif user_choice == 'Chat with your Brain':
    # Display model and temperature selection only when asking questions
    st.sidebar.title("Configuration")
    st.sidebar.markdown(
        "Choose your model and temperature for asking questions.")
    if st.secrets.self_hosted != "false":
        st.session_state['model'] = st.sidebar.selectbox(
        "Select Model", models, index=(models).index(st.session_state['model']))
    else:
        st.sidebar.write("**Model**: gpt-3.5-turbo")
        st.sidebar.write("**Self Host to unlock more models such as claude-v1 and GPT4**")
        st.session_state['model'] = "gpt-3.5-turbo"
    st.session_state['temperature'] = st.sidebar.slider(
        "Select Temperature", 0.0, 1.0, st.session_state['temperature'], 0.1)
    if st.secrets.self_hosted != "false":
        st.session_state['max_tokens'] = st.sidebar.slider(
            "Select Max Tokens", 256, 2048, st.session_state['max_tokens'], 2048)
    else:
        st.session_state['max_tokens'] = 100
    
    chat_with_doc(st.session_state['model'], vector_store, stats_db=supabase)
elif user_choice == 'Forget':
    st.sidebar.title("Configuration")

    brain(supabase)
elif user_choice == 'Explore':
    st.sidebar.title("Configuration")
    view_document(supabase)

st.markdown("---\n\n")
