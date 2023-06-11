import os
from typing import Any, Dict, List

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI, ChatVertexAI
from langchain.chat_models.anthropic import ChatAnthropic
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import VertexAI
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import SupabaseVectorStore
from llm import LANGUAGE_PROMPT
from logger import get_logger
from models.chats import ChatMessage

from supabase import Client, create_client

logger = get_logger(__name__)


class CustomSupabaseVectorStore(SupabaseVectorStore):
    '''A custom vector store that uses the match_vectors table instead of the vectors table.'''
    user_id: str

    def __init__(self, client: Client, embedding: OpenAIEmbeddings, table_name: str, user_id: str = "none"):
        super().__init__(client, embedding, table_name)
        self.user_id = user_id

    def similarity_search(
        self,
        query: str,
        user_id: str = "none",
        table: str = "match_vectors",
        k: int = 4,
        threshold: float = 0.5,
        file_sha1s: str = None,  # comma separated list of file shas
        **kwargs: Any
    ) -> List[Document]:
        vectors = self._embedding.embed_documents([query])
        query_embedding = vectors[0]
        logger.info(f'file_sha1s : {file_sha1s}')
        if file_sha1s:
            res = self._client.rpc(
                table,
                {
                    "query_embedding": query_embedding,
                    "match_count": k * 2,  # increase the match count to account for the filter
                    "p_user_id": self.user_id,
                },
            ).execute()
            documents = [
                Document(
                    metadata=search.get("metadata", {}),  # type: ignore
                    page_content=search.get("content", ""),
                )
                for search in res.data
                if search.get("content") and search.get("metadata", {}).get("file_sha1") in file_sha1s
            ]
        else:
            res = self._client.rpc(
                table,
                {
                    "query_embedding": query_embedding,
                    "match_count": k,
                    "p_user_id": self.user_id,
                },
            ).execute()
            documents = [
                Document(
                    metadata=search.get("metadata", {}),  # type: ignore
                    page_content=search.get("content", ""),
                )
                for search in res.data
                if search.get("content")
            ]

        return documents


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


def get_qa_llm(chat_message: ChatMessage, user_id: str, user_openai_api_key: str, with_sources: bool = True):
    '''Get the question answering language model.'''
    openai_api_key, anthropic_api_key, supabase_url, supabase_key = get_environment_variables()

    '''User can override the openai_api_key'''
    if user_openai_api_key is not None and user_openai_api_key != "":
        openai_api_key = user_openai_api_key

    supabase_client, embeddings = create_clients_and_embeddings(
        openai_api_key, supabase_url, supabase_key)

    vector_store = CustomSupabaseVectorStore(
        supabase_client, embeddings, table_name="vectors", user_id=user_id)

    if with_sources:
        memory = AnswerConversationBufferMemory(
            memory_key="chat_history", return_messages=True)
    else:
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True)

    ConversationalRetrievalChain.prompts = LANGUAGE_PROMPT

    qa = None
    # this overwrites the built-in prompt of the ConversationalRetrievalChain
    ConversationalRetrievalChain.prompts = LANGUAGE_PROMPT

    retriever = vector_store.as_retriever()
    # chat with multiple files if file_sha1s is not empty
    if chat_message.file_sha1s:
        retriever.search_kwargs = {
            "file_sha1s": ','.join(chat_message.file_sha1s)
        }
    if chat_message.model.startswith("gpt"):
        qa = ConversationalRetrievalChain.from_llm(
            ChatOpenAI(
                model_name=chat_message.model, openai_api_key=openai_api_key,
                temperature=chat_message.temperature, max_tokens=chat_message.max_tokens),
            retriever, memory=memory, verbose=True,
            return_source_documents=with_sources,
            max_tokens_limit=1024)
    elif chat_message.model.startswith("vertex"):
        qa = ConversationalRetrievalChain.from_llm(
            ChatVertexAI(), retriever, memory=memory, verbose=False,
            return_source_documents=with_sources, max_tokens_limit=1024)
    elif anthropic_api_key and chat_message.model.startswith("claude"):
        qa = ConversationalRetrievalChain.from_llm(
            ChatAnthropic(
                model=chat_message.model, anthropic_api_key=anthropic_api_key, temperature=chat_message.temperature, max_tokens_to_sample=chat_message.max_tokens),
            retriever, memory=memory, verbose=False,
            return_source_documents=with_sources,
            max_tokens_limit=102400)
    return qa
