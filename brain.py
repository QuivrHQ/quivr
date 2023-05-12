import streamlit as st
import numpy as np

def brain(supabase):
    ## List all documents
    response = supabase.table("documents").select("name:metadata->>file_name, size:metadata->>file_size", count="exact").execute()
    
    documents = response.data  # Access the data from the response

    # Convert each dictionary to a tuple of items, then to a set to remove duplicates, and then back to a dictionary
    unique_data = [dict(t) for t in set(tuple(d.items()) for d in documents)]

    # Sort the list of documents by size in decreasing order
    unique_data.sort(key=lambda x: int(x['size']), reverse=True)

    # Display some metrics at the top of the page
    col1, col2 = st.columns(2)
    col1.metric(label="Total Documents", value=len(unique_data))
    col2.metric(label="Total Size (bytes)", value=sum(int(doc['size']) for doc in unique_data))

    for document in unique_data:
        # Create a unique key for each button by using the document name
        button_key = f"delete_{document['name']}"

        # Display the document name, size and the delete button on the same line
        col1, col2, col3 = st.columns([3, 1, 1])
        col1.markdown(f"**{document['name']}** ({document['size']} bytes)")
        
        if col2.button('❌', key=button_key):
            delete_document(supabase, document['name'])

def delete_document(supabase, document_name):
    # Delete the document from the database
    response = supabase.table("documents").delete().match({"metadata->>file_name": document_name}).execute()
    # Check if the deletion was successful
    if len(response.data) > 0:
        st.write(f"✂️ {document_name} was deleted.")
    else:
        st.write(f"❌ {document_name} was not deleted.")
