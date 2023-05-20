import anthropic
import streamlit as st
from streamlit.logger import get_logger
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from langchain.chat_models import ChatAnthropic
from langchain.vectorstores import SupabaseVectorStore
from stats import add_usage
from utils import similarity_search, llm_evaluate_summaries, supabase_client

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


def get_qa_llm(vector_store: SupabaseVectorStore):
    model = st.session_state['model']
    if model.startswith("gpt"):
        logger.info('Using OpenAI model %s', model)
        qa = ConversationalRetrievalChain.from_llm(
            OpenAI(
                model_name=st.session_state['model'], openai_api_key=openai_api_key, temperature=st.session_state['temperature'], max_tokens=st.session_state['max_tokens']), vector_store.as_retriever(), memory=memory, verbose=True, max_tokens_limit=1024)
    elif anthropic_api_key and model.startswith("claude"):
        logger.info('Using Anthropics model %s', model)
        qa = ConversationalRetrievalChain.from_llm(
            ChatAnthropic(
                model=st.session_state['model'], anthropic_api_key=anthropic_api_key, temperature=st.session_state['temperature'], max_tokens_to_sample=st.session_state['max_tokens']), vector_store.as_retriever(), memory=memory, verbose=True, max_tokens_limit=102400)
    return qa


def chat_with_doc(vector_store: SupabaseVectorStore, stats_db):
    model = st.session_state['model']
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

    summary_search = st.checkbox('With summary search')

    if clear_history:
        st.session_state['chat_history'] = []
        st.experimental_rerun()

    if button:
        qa = None
        if not st.session_state["overused"]:
            add_usage(stats_db, "chat", "prompt" + question,
                      {"model": model, "temperature": st.session_state['temperature']})
            qa = get_qa_llm(vector_store)

            st.session_state['chat_history'].append(("You", question))

            # Summary Search flow
            additional_context = ''
            if summary_search:
                # 1. get summaries from the vector store based on question
                summaries = similarity_search(
                    question, table='match_summaries')
                # 2. evaluate summaries against the question
                evaluations = llm_evaluate_summaries(question, summaries)
                # 3. pull in the top documents from summaries
                logger.info('Evaluations: %s', evaluations)
                if evaluations:
                    reponse = supabase_client.from_('documents').select(
                        '*').in_('id', values=[e['document_id'] for e in evaluations]).execute()
                # 4. use top docs as additional context
                    additional_context = '---\nAdditional Context={}'.format(
                        '---\n'.join(data['content'] for data in reponse.data)
                    ) + '\n'

            # Generate model's response and add it to chat history
            model_response = qa(
                {"question": additional_context + question if summary_search else question})
            logger.info('Result: %s', model_response)

            st.session_state['chat_history'].append(
                ("Quivr", model_response["answer"]))

            # Display chat history
            st.empty()
            for speaker, text in st.session_state['chat_history']:
                st.markdown(f"**{speaker}:** {text}")
        else:
            st.error(
                "You have used all your free credits. Please try again later or self host.")

    if count_button:
        st.write(count_tokens(question, model))
