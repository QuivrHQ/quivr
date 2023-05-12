import streamlit as st


def sidebar(supabase):
    st.sidebar.title("Database Information") 
    number_of_docs = number_of_documents(supabase)
    st.sidebar.markdown(f"**Docs in DB:**  {number_of_docs}")

def number_of_documents(supabase):
    documents = supabase.table("documents").select("id", count="exact").execute()
    return documents.count