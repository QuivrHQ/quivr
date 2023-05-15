import streamlit as st
from supabase import Client, create_client

supabase_url = st.secrets.supabase_url
supabase_key = st.secrets.supabase_service_key
openai_api_key = st.secrets.openai_api_key

db_client: Client = create_client(supabase_url, supabase_key)


def add_prompt(prompt_title, prompt, prompt_description=None, ):
    ''' 
    If there is a prompt description, add it to the database
    Else, add the prompt without the description
    '''
    if prompt and prompt_description:
        response = db_client.table("prompts").upsert({"prompt_title": prompt_title, "prompt": prompt, "prompt_description": prompt_description}, on_conflict="prompt_title").execute()
    else:
        response = db_client.table("prompts").upsert({"prompt_title": prompt_title, "prompt": prompt}, on_conflict="prompt_title").execute()

    if response.data == []:
        return "Error in adding prompt"
    else:
        return "Prompt added successfully"

def update_prompt(prompt_title, prompt=None, prompt_description=None):
    
    '''
    If there is a prompt description, add it to the database
    Else, update the prompt without the description
    '''
    if prompt and prompt_description:
        response = db_client.table("prompts").upsert({"prompt_title": prompt_title, "prompt": prompt, "prompt_description": prompt_description}, on_conflict="prompt_title").execute()
    elif prompt_description and prompt is None:
        response = db_client.table("prompts").upsert({"prompt_title": prompt_title, "prompt_description": prompt_description}, on_conflict="prompt_title").execute()
    elif prompt and prompt_description is None:
        response = db_client.table("prompts").upsert({"prompt_title": prompt_title, "prompt": prompt}, on_conflict="prompt_title").execute()

    if response.data == []:
        return "Error in updating prompt"
    else:
        return "Prompt updated successfully"


def delete_prompt(prompt_title):
    
    response = db_client.table("prompts").delete().eq("prompt_title", prompt_title).execute()
    ## If there is an error, return the error message
    if response.data == []:
        return "Prompt not found"
    else:
        return "Prompt deleted successfully"


def get_all_prompt_data(_db_client):

    response = db_client.table("prompts").select("prompt_title", "prompt", "prompt_description").execute()
    
    if response.data != []:
        prompt_data = [d for d in response.data]
        return prompt_data
    else:
        return "No prompts found"
    

def get_all_prompt_titles(_db_client):

    response = db_client.table("prompts").select("prompt_title").execute()

    if response.data != []:
        prompt_titles = [title["prompt_title"] for title in response.data]
        return prompt_titles
    else:
        return "No prompt titles found"
    
def get_prompt_from_title(prompt_title, db_client):

    response = db_client.table("prompts").select("prompt").eq("prompt_title", prompt_title).execute()
    if response.data != []:
        return response.data[0]["prompt"]
    else:
        return "Prompt not found"


def manage_prompts(db_client):
    ## Set streamlit sidebar to provide options for managing prompts including adding, updating, deleting and viewing prompts
    st.sidebar.title("Prompt Manager")
    st.sidebar.markdown(
        "Create, update, delete and view prompts for your brain.")
    prompt_manager_options = st.sidebar.radio(
        "Choose an action", ('Add Prompt', 'Update Prompt', 'Delete Prompt', 'View Prompts'))
    st.sidebar.markdown("---\n\n")

    ## If user chooses to add a prompt, provide a text box for the prompt title, prompt and prompt description
    if prompt_manager_options == 'Add Prompt':
        st.title("Add a Prompt")
        prompt_title = st.text_input("Prompt Title")
        prompt = st.text_area("Prompt")
        prompt_description = st.text_area("Prompt Description")
        if st.button("Add Prompt"):
            st.write(add_prompt(prompt_title, prompt, prompt_description))
            st.markdown("---\n\n")
    ## If user chooses to update a prompt, provide a text box for the prompt title, prompt and prompt description
    elif prompt_manager_options == 'Update Prompt':
        st.title("Update a Prompt")
        prompt_title = st.selectbox("Prompt Title", get_all_prompt_titles(db_client))
        prompt = st.text_area("Prompt", get_prompt_from_title(prompt_title, db_client))
        prompt_description = st.text_area("Prompt Description")
        if st.button("Update Prompt"):
            st.write(update_prompt(prompt_title, prompt, prompt_description))
            st.markdown("---\n\n")
    ## If user chooses to delete a prompt, provide a text box for the prompt title
    elif prompt_manager_options == 'Delete Prompt':
        st.title("Delete a Prompt")
        prompt_title = st.selectbox("Prompt Title", get_all_prompt_titles(db_client))
        if st.button("Delete Prompt"):
            st.write(delete_prompt(prompt_title))
            st.markdown("---\n\n")
    ## If user chooses to view all prompts, display all prompts
    elif prompt_manager_options == 'View Prompts':
        st.title("View Prompts")
        st.dataframe(get_all_prompt_data(db_client), use_container_width=True)
        st.markdown("---\n\n")
    