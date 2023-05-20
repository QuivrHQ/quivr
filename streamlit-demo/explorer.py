import streamlit as st


def view_document(supabase):
    # Get the document from the database
    response = supabase.table("documents").select("content").execute()
    st.write("**This feature is in active development**")
    # Display a list of elements from the documents
    # If the user clicks on an element, display the content of the document
    for document in response.data:
        if st.button(document['content'][:50].replace("\n", " ")):
            continue
