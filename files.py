import streamlit as st
from loaders.audio import  process_audio
from loaders.txt import process_txt
from loaders.csv import process_csv
from loaders.markdown import process_markdown
from utils import compute_sha1_from_content

def file_uploader(supabase, openai_key, vector_store):
    files = st.file_uploader("Upload a file", accept_multiple_files=True, type=["txt", "csv", "md", "m4a", "mp3", "webm", "mp4", "mpga", "wav", "mpeg"])
    if st.button("Add to Database"):
        if files is not None:
             for file in files:
                if file_already_exists(supabase, file):
                    st.write(f"😎 {file.name} is already in the database.")
                else: 
                    if file.name.endswith(".txt"):
                        process_txt(vector_store, file)
                        st.write(f"✅ {file.name} ")
                    elif file.name.endswith((".m4a", ".mp3", ".webm", ".mp4", ".mpga", ".wav", ".mpeg")):
                        process_audio(openai_key,vector_store, file)
                        st.write(f"✅ {file.name} ")
                    elif file.name.endswith(".csv"):
                        process_csv(vector_store, file)
                        st.write(f"✅ {file.name} ")
                    elif file.name.endswith(".md"):
                        process_markdown(vector_store, file)
                        st.write(f"✅ {file.name} ")
                    else:
                        st.write(f"❌ {file.name} is not a valid file type.")

def file_already_exists(supabase, file):
    file_sha1 = compute_sha1_from_content(file.getvalue())
    response = supabase.table("documents").select("id").eq("metadata->>file_sha1", file_sha1).execute()
    if len(response.data) > 0:
        return True
    else:
        return False
