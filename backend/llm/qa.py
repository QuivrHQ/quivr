import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from supabase import create_client, Client
from langchain.llms import OpenAI
from langchain.chat_models.anthropic import ChatAnthropic

from utils import ChatMessage
import llm.LANGUAGE_PROMPT as LANGUAGE_PROMPT


openai_api_key = os.environ.get("OPENAI_API_KEY")
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
supabase_client: Client = create_client(supabase_url, supabase_key)
vector_store = SupabaseVectorStore(
    supabase_client, embeddings, table_name="documents")
memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)


def get_qa_llm(chat_message: ChatMessage):
    qa = None
    # this overwrites the built-in prompt of the ConversationalRetrievalChain
    ConversationalRetrievalChain.prompts = LANGUAGE_PROMPT
    if chat_message.model.startswith("gpt"):
        qa = ConversationalRetrievalChain.from_llm(
            OpenAI(
                model_name=chat_message.model, openai_api_key=openai_api_key, temperature=chat_message.temperature, max_tokens=chat_message.max_tokens), vector_store.as_retriever(), memory=memory, verbose=False, max_tokens_limit=1024)
    elif anthropic_api_key and chat_message.model.startswith("claude"):
        qa = ConversationalRetrievalChain.from_llm(
            ChatAnthropic(
                model=chat_message.model, anthropic_api_key=anthropic_api_key, temperature=chat_message.temperature, max_tokens_to_sample=chat_message.max_tokens), vector_store.as_retriever(), memory=memory, verbose=False, max_tokens_limit=102400)
    return qa
