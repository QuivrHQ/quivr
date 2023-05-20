import streamlit as st
from supabase import Client
import json


def view_document(supabase: Client):
    # Get the document from the database
    response = supabase.table("documents").select('id', "content").execute()
    # Display a list of elements from the documents
    # If the user clicks on an element, display the content of the document
    for document in response.data:
        if st.button(document['content'][:50].replace("\n", " ")):
            continue


def view_summaries(supabase: Client):
    # Get the document from the database
    response = supabase.table("summaries").select(
        'document_id', 'content', 'metadata').execute()
    st.table([{
        'document_id': data['document_id'],
        'content': data['content'],
        'metadata': json.dumps(data['metadata'])}
        for data in response.data])
