import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI


memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


def chat_with_doc(openai_api_key,vector_store):
    question = st.text_input("## Ask a question")
    temperature = st.session_state.get("temperature", 0.0)
    model = st.session_state.get("model", "gpt-3.5-turbo")
    button = st.button("Ask")
    if button:
        qa = ConversationalRetrievalChain.from_llm(OpenAI(model_name=model, openai_api_key=openai_api_key, temperature=temperature), vector_store.as_retriever(), memory=memory)
        result = qa({"question": question})
        st.write(result["answer"])