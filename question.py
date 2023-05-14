import streamlit as st
from streamlit.logger import get_logger
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chat_models import ChatAnthropic
from langchain.vectorstores import SupabaseVectorStore

memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)
openai_api_key = st.secrets.openai_api_key
anthropic_api_key = st.secrets.anthropic_api_key
logger = get_logger(__name__)


def chat_with_doc(model, vector_store: SupabaseVectorStore):
    question = st.text_area("## Ask a question")
    button = st.button("Ask")
    if button:
        if model.startswith("gpt"):
            logger.info('Using OpenAI model %s', model)
            qa = ConversationalRetrievalChain.from_llm(
                OpenAI(
                    model_name=st.session_state['model'], openai_api_key=openai_api_key, temperature=st.session_state['temperature'], max_tokens=st.session_state['max_tokens']), vector_store.as_retriever(), memory=memory, verbose=True)
            result = qa({"question": question})
            logger.info('Result: %s', result)
            st.write(result["answer"])
        elif anthropic_api_key and model.startswith("claude"):
            logger.info('Using Anthropics model %s', model)
            qa = ConversationalRetrievalChain.from_llm(
                ChatAnthropic(
                    model=st.session_state['model'], anthropic_api_key=anthropic_api_key, temperature=st.session_state['temperature'], max_tokens_to_sample=st.session_state['max_tokens']), vector_store.as_retriever(), memory=memory, verbose=True, max_tokens_limit=102400)
            result = qa({"question": question})
            logger.info('Result: %s', result)
            st.write(result["answer"])
