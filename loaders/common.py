import tempfile
from utils import compute_sha1_from_file
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def process_file(vector_store, file, loader_class, file_suffix):
    documents = []
    file_sha = ""
    with tempfile.NamedTemporaryFile(delete=True, suffix=file_suffix) as tmp_file:
        tmp_file.write(file.getvalue())
        tmp_file.flush()

        loader = loader_class(tmp_file.name)
        documents = loader.load()
        file_sha1 = compute_sha1_from_file(tmp_file.name)
    
    chunk_size = st.session_state['chunk_size']
    chunk_overlap = st.session_state['chunk_overlap']

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    documents = text_splitter.split_documents(documents)

    # Add the document sha1 as metadata to each document
    docs_with_metadata = [Document(page_content=doc.page_content, metadata={"file_sha1": file_sha1}) for doc in documents]
    
    vector_store.add_documents(docs_with_metadata)
    return 