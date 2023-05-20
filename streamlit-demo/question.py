import anthropic
import streamlit as st
from streamlit.logger import get_logger
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chat_models import ChatAnthropic
from langchain.vectorstores import SupabaseVectorStore
from stats import add_usage

memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)
openai_api_key = st.secrets.openai_api_key
anthropic_api_key = st.secrets.anthropic_api_key
logger = get_logger(__name__)


def count_tokens(question, model):
    count = f'Words: {len(question.split())}'
    if model.startswith("claude"):
        count += f' | Tokens: {anthropic.count_tokens(question)}'
    return count


def chat_with_doc(model, vector_store: SupabaseVectorStore, stats_db):
    
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []
        
    
    
    question = st.text_area("## Ask a question")
    columns = st.columns(3)
    with columns[0]:
        button = st.button("Ask")
    with columns[1]:
        count_button = st.button("Count Tokens", type='secondary')
    with columns[2]:
        clear_history = st.button("Clear History", type='secondary')
    
    
    
    if clear_history:
        # Clear memory in Langchain
        memory.clear()
        st.session_state['chat_history'] = []
        st.experimental_rerun()

    if button:
        qa = None
        if not st.session_state["overused"]:
            add_usage(stats_db, "chat", "prompt" + question, {"model": model, "temperature": st.session_state['temperature']})
            if model.startswith("gpt"):
                logger.info('Using OpenAI model %s', model)
                qa = ConversationalRetrievalChain.from_llm(
                    OpenAI(
                        model_name=st.session_state['model'], openai_api_key=openai_api_key, temperature=st.session_state['temperature'], max_tokens=st.session_state['max_tokens']), vector_store.as_retriever(), memory=memory, verbose=True)
            elif anthropic_api_key and model.startswith("claude"):
                logger.info('Using Anthropics model %s', model)
                qa = ConversationalRetrievalChain.from_llm(
                    ChatAnthropic(
                        model=st.session_state['model'], anthropic_api_key=anthropic_api_key, temperature=st.session_state['temperature'], max_tokens_to_sample=st.session_state['max_tokens']), vector_store.as_retriever(), memory=memory, verbose=True, max_tokens_limit=102400)
            
            
            st.session_state['chat_history'].append(("You", question))

            # Generate model's response and add it to chat history
            model_response = qa({"question": question})
            logger.info('Result: %s', model_response)

            st.session_state['chat_history'].append(("Quivr", model_response["answer"]))

            # Display chat history
            st.empty()
            for speaker, text in st.session_state['chat_history']:
                st.markdown(f"**{speaker}:** {text}")
        else:
            st.error("You have used all your free credits. Please try again later or self host.")
        
    if count_button:
        st.write(count_tokens(question, model))
