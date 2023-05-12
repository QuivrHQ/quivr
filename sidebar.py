import streamlit as st


def sidebar(supabase):
    st.sidebar.title("Configuration") 
    
    
    ## Get the number of documents in the database
    number_of_docs = number_of_documents(supabase)
    ## Display the number of documents in the database
    st.sidebar.markdown(f"**Docs in DB:**  {number_of_docs}")
    
    ## Allow user to choose model between gpt-3.5-turbo and gpt-4
    model = st.sidebar.selectbox("Select Model", ["gpt-3.5-turbo", "gpt-4"])
    ## Allow user to choose temperature between 0.0 and 1.0
    temperature = st.sidebar.slider("Select Temperature", 0.0, 1.0, 0.0, 0.1)
    ## Allow user to choose chunk_size between 100 and 1000
    chunk_size = st.sidebar.slider("Select Chunk Size", 100, 1000, 500, 50)
    ## Allow user to choose chunk_overlap between 0 and 100
    chunk_overlap = st.sidebar.slider("Select Chunk Overlap", 0, 100, 0, 10)


    ## Save the user's choices
    st.session_state.model = model
    st.session_state.temperature = temperature
    st.session_state.chunk_size = chunk_size
    st.session_state.chunk_overlap = chunk_overlap

def number_of_documents(supabase):
    ## Get the number of documents in the database
    documents = supabase.table("documents").select("id", count="exact").execute()
    return documents.count