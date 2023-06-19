import os
from typing import Any, Dict, List

from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.router.llm_router import (LLMRouterChain,
                                                RouterOutputParser)
from langchain.chains.router.multi_prompt_prompt import \
    MULTI_PROMPT_ROUTER_TEMPLATE
from langchain.chat_models import ChatOpenAI, ChatVertexAI
from langchain.chat_models.anthropic import ChatAnthropic
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI, VertexAI
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import SupabaseVectorStore
from llm.prompt import LANGUAGE_PROMPT
from llm.prompt.CONDENSE_PROMPT import CONDENSE_QUESTION_PROMPT
from models.chats import ChatMessage
from supabase import Client, create_client
from vectorstore.supabase import CustomSupabaseVectorStore


class AnswerConversationBufferMemory(ConversationBufferMemory):
    """ref https://github.com/hwchase17/langchain/issues/5630#issuecomment-1574222564"""
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        return super(AnswerConversationBufferMemory, self).save_context(
            inputs, {'response': outputs['answer']})


def get_environment_variables():
    '''Get the environment variables.'''
    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
    
    return openai_api_key, anthropic_api_key, supabase_url, supabase_key

def create_clients_and_embeddings(openai_api_key, supabase_url, supabase_key):
    '''Create the clients and embeddings.'''
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    supabase_client = create_client(supabase_url, supabase_key)
    
    return supabase_client, embeddings

def get_chat_history(inputs) -> str:
    res = []
    for human, ai in inputs:
        res.append(f"{human}:{ai}\n")
    return "\n".join(res)

def get_qa_llm(chat_message: ChatMessage, user_id: str, user_openai_api_key: str, with_sources: bool = False):
    '''Get the question answering language model.'''
    openai_api_key, anthropic_api_key, supabase_url, supabase_key = get_environment_variables()

    '''User can override the openai_api_key'''
    if user_openai_api_key is not None and user_openai_api_key != "":
        openai_api_key = user_openai_api_key

    supabase_client, embeddings = create_clients_and_embeddings(openai_api_key, supabase_url, supabase_key)
    
    vector_store = CustomSupabaseVectorStore(
        supabase_client, embeddings, table_name="vectors", user_id=user_id)

    
    
    qa = None
        
    if chat_message.model.startswith("gpt"):
        llm = ChatOpenAI(temperature=0, model_name=chat_message.model)
        question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
        doc_chain = load_qa_chain(llm, chain_type="stuff")

        qa = ConversationalRetrievalChain(
                retriever=vector_store.as_retriever(),
                max_tokens_limit=chat_message.max_tokens, question_generator=question_generator,
                combine_docs_chain=doc_chain, get_chat_history=get_chat_history)
    elif chat_message.model.startswith("vertex"):
        qa = ConversationalRetrievalChain.from_llm(
            ChatVertexAI(), vector_store.as_retriever(), verbose=True, 
            return_source_documents=with_sources, max_tokens_limit=1024,question_generator=question_generator,
                combine_docs_chain=doc_chain)
    elif anthropic_api_key and chat_message.model.startswith("claude"):
        qa = ConversationalRetrievalChain.from_llm(
            ChatAnthropic(
                model=chat_message.model, anthropic_api_key=anthropic_api_key, temperature=chat_message.temperature, max_tokens_to_sample=chat_message.max_tokens), 
                vector_store.as_retriever(), verbose=False, 
                return_source_documents=with_sources,
                max_tokens_limit=102400)
        qa.combine_docs_chain = load_qa_chain(ChatAnthropic(), chain_type="stuff", prompt=LANGUAGE_PROMPT.QA_PROMPT)
    
    return qa
