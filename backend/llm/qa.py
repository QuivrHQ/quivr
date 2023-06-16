import os

from langchain.chains import ConversationalRetrievalChain
from langchain.chains.conversational_retrieval.prompts import \
    CONDENSE_QUESTION_PROMPT
from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI, ChatVertexAI
from langchain.chat_models.anthropic import ChatAnthropic
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from llm.callback import StreamingCallbackHandler
from llm.LANGUAGE_PROMPT import QA_PROMPT
from llm.vector_store import CustomSupabaseVectorStore
from models.chats import ChatMessage
from supabase import create_client


def get_environment_variables():
    """Get the environment variables."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")

    return openai_api_key, anthropic_api_key, supabase_url, supabase_key


def create_clients_and_embeddings(openai_api_key, supabase_url, supabase_key):
    """Create the clients and embeddings."""
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    supabase_client = create_client(supabase_url, supabase_key)

    return supabase_client, embeddings


def get_vector_store_and_memory(supabase_client, embeddings, user_id):
    vector_store = CustomSupabaseVectorStore(
        supabase_client, embeddings, table_name="vectors", user_id=user_id)
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True)
    return vector_store, memory


def get_qa_llm(
    chat_message: ChatMessage,
    user_id: str,
    user_openai_api_key: str,
    with_sources: bool = False,
    with_streaming: bool = False,
    callback_handler=None,
):
    '''User can override the openai_api_key'''
    (
        openai_api_key,
        anthropic_api_key,
        supabase_url,
        supabase_key,
    ) = get_environment_variables()

    if user_openai_api_key is not None and user_openai_api_key != "":
        openai_api_key = user_openai_api_key

    supabase_client, embeddings = create_clients_and_embeddings(
        openai_api_key, supabase_url, supabase_key
    )

    vector_store, memory = get_vector_store_and_memory(
        supabase_client, embeddings, user_id
    )

    qa = None
    # this overwrites the built-in prompt of the ConversationalRetrievalChain

    if chat_message.model.startswith("gpt"):
        if with_streaming:
            llm = ChatOpenAI(temperature=0)

            streaming_llm = ChatOpenAI(
                model_name=chat_message.model,
                openai_api_key=openai_api_key,
                temperature=chat_message.temperature,
                max_tokens=chat_message.max_tokens,
                streaming=with_streaming,
                callbacks=[callback_handler] if callback_handler else [],
            )

            question_generator = LLMChain(
                llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
            docs_chain = load_qa_chain(
                streaming_llm,
                chain_type="stuff",
                prompt=QA_PROMPT,
            )

            qa = ConversationalRetrievalChain(
                retriever=vector_store.as_retriever(),
                combine_docs_chain=docs_chain,
                question_generator=question_generator,
                verbose=True,
                max_tokens_limit=1024,
            )
        else:
            qa = ConversationalRetrievalChain.from_llm(
                ChatOpenAI(
                    model_name=chat_message.model,
                    openai_api_key=openai_api_key,
                    temperature=chat_message.temperature,
                    max_tokens=chat_message.max_tokens,
                ),
                vector_store.as_retriever(),
                memory=memory,
                verbose=True,
                return_source_documents=with_sources,
                max_tokens_limit=1024,
            )

            qa.combine_docs_chain = load_qa_chain(
                ChatOpenAI(), chain_type="stuff", prompt=QA_PROMPT
            )

    elif chat_message.model.startswith("vertex"):
        qa = ConversationalRetrievalChain.from_llm(
            ChatVertexAI(),
            vector_store.as_retriever(),
            memory=memory,
            verbose=True,
            return_source_documents=with_sources,
            max_tokens_limit=1024,
        )

        qa.combine_docs_chain = load_qa_chain(
            ChatVertexAI(), chain_type="stuff", prompt=QA_PROMPT
        )

    elif anthropic_api_key and chat_message.model.startswith("claude"):
        qa = ConversationalRetrievalChain.from_llm(
            ChatAnthropic(
                model=chat_message.model,
                anthropic_api_key=anthropic_api_key,
                temperature=chat_message.temperature,
                max_tokens_to_sample=chat_message.max_tokens,
            ),
            vector_store.as_retriever(),
            memory=memory,
            verbose=False,
            return_source_documents=with_sources,
            max_tokens_limit=102400,
        )

        qa.combine_docs_chain = load_qa_chain(
            ChatAnthropic(), chain_type="stuff", prompt=QA_PROMPT
        )

    return qa
