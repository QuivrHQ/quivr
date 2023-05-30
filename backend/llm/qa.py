import os
from typing import (TYPE_CHECKING, Any, Iterable, List, Optional, Tuple, Type,
                    Union)

import llm.LANGUAGE_PROMPT as LANGUAGE_PROMPT
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.anthropic import ChatAnthropic
from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import SupabaseVectorStore
from langchain.vectorstores.base import VectorStore
from langchain.vectorstores.utils import maximal_marginal_relevance
from supabase import Client, create_client
from utils import ChatMessage


class CustomSupabaseVectorStore(SupabaseVectorStore):
    def similarity_search(
        self, query: str, user_id: str = "tata", table: str = "match_vectors", k: int = 4, threshold: float = 0.5, **kwargs: Any
    ) -> List[Document]:
        vectors = self._embedding.embed_documents([query])
        query_embedding = vectors[0]
        res = self._client.rpc(
            table,
            {
                "query_embedding": query_embedding,
                "match_count": k,
                "p_user_id": user_id,
            },
        ).execute()

        match_result = [
            (
                Document(
                    metadata=search.get("metadata", {}),  # type: ignore
                    page_content=search.get("content", ""),
                ),
                search.get("similarity", 0.0),
            )
            for search in res.data
            if search.get("content")
        ]

        documents = [doc for doc, _ in match_result]

        return documents

openai_api_key = os.environ.get("OPENAI_API_KEY")
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
supabase_client: Client = create_client(supabase_url, supabase_key)
vector_store = CustomSupabaseVectorStore(
    supabase_client, embeddings, table_name="vectors")
memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True)


def get_qa_llm(chat_message: ChatMessage):
    qa = None
    # this overwrites the built-in prompt of the ConversationalRetrievalChain
    ConversationalRetrievalChain.prompts = LANGUAGE_PROMPT
    if chat_message.model.startswith("gpt"):
        qa = ConversationalRetrievalChain.from_llm(
            ChatOpenAI(
                model_name=chat_message.model, openai_api_key=openai_api_key, 
                temperature=chat_message.temperature, max_tokens=chat_message.max_tokens), 
                vector_store.as_retriever(), memory=memory, verbose=True, 
                max_tokens_limit=1024)
    elif anthropic_api_key and chat_message.model.startswith("claude"):
        qa = ConversationalRetrievalChain.from_llm(
            ChatAnthropic(
                model=chat_message.model, anthropic_api_key=anthropic_api_key, temperature=chat_message.temperature, max_tokens_to_sample=chat_message.max_tokens), vector_store.as_retriever(), memory=memory, verbose=False, max_tokens_limit=102400)
    return qa
