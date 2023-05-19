import streamlit as st

def show_document(document):
    st.write("**Document Content**")
    st.write(document)

def view_document(supabase):
    # Get the document from the database
    response = supabase.table("documents").select("content").execute()
    st.write("**This feature is in active development**")
    st.write("**Document List**")

    # Display a list of elements from the documents
    # If the user clicks on an element, display the content of the document
    selected_document = None
    for index, document in enumerate(response.data):
        if st.button(document['content'][:50].replace("\n", " "), key=f"document_button_{index}"):
            selected_document = document['content']
    
    if selected_document:
        show_document(selected_document)
