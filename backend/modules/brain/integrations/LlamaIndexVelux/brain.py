import os
import json
import time
from typing import AsyncIterable
from uuid import UUID

from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from llama_index.core import (
    Settings,
    load_index_from_storage,
    StorageContext,
)

# from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.chat_engine.types import ChatMode
from llama_index.core.llms import ChatMessage, MessageRole
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.core.prompts import PromptTemplate, PromptType

# from llama_index.core.ingestion import (
#     DocstoreStrategy,
#     IngestionCache,
#     IngestionPipeline,
# )
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker

# from llama_index.readers.google import GoogleDriveReader
# from llama_index.storage.kvstore.redis import RedisKVStore as RedisCache
# from llama_index.storage.docstore.redis import RedisDocumentStore
# from llama_index.vector_stores.redis import RedisVectorStore

from modules.brain.knowledge_brain_qa import KnowledgeBrainQA
from modules.chat.dto.chats import ChatQuestion

data_directory = "/data/"
folder_name = "Documents/Manufacturers/Velux-UK"
index_data = os.path.join(data_directory, folder_name, "index-data")

storage_context = None
index = None
reranker = None

if os.path.exists(index_data):
    try:
        if not storage_context:
            print("####### Starting loading storage context... #######")
            start_time = time.time()  # Record the start time

            storage_context = StorageContext.from_defaults(
                persist_dir=index_data
            )

            end_time = time.time()  # Record the end time
            elapsed_time = end_time - start_time  # Calculate elapsed time
            print(
                f"####### Finishing loading storage context... in {elapsed_time:.2f} seconds #######"
            )
        if not index:
            print("####### Starting loading index from storage... #######")
            start_time = time.time()  # Record the start time

            index = load_index_from_storage(
                storage_context=storage_context, index_id="vector_index"
            )

            end_time = time.time()  # Record the end time
            elapsed_time = end_time - start_time  # Calculate elapsed time
            print(
                f"####### Finishing loading index from storage... in {elapsed_time:.2f} seconds #######"
            )
        if not reranker:
            print("####### Starting loading reranker... #######")
            start_time = time.time()  # Record the start time

            reranker = FlagEmbeddingReranker(
                top_n=7, model="BAAI/bge-reranker-large", use_fp16=True
            )

            end_time = time.time()  # Record the end time
            elapsed_time = end_time - start_time  # Calculate elapsed time
            print(
                f"####### Finishing loading reranker... in {elapsed_time:.2f} seconds #######"
            )
    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(f"### {e}")
else:
    print("### No index found...")

embed_model = OpenAIEmbedding(model="text-embedding-3-small")
llm = OpenAI(model="gpt-4-turbo-preview")

Settings.llm = llm
Settings.embed_model = embed_model


class LlamaIndexVeluxUK(KnowledgeBrainQA):
    """This is a first implementation of LlamaIndex recursive retriever RAG class. it is a KnowledgeBrainQA has the data is stored locally.
    It is going to call the Data Store internally to get the data.

    Args:
        KnowledgeBrainQA (_type_): A brain that store the knowledge internaly
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )
        self._storage_context = storage_context
        self._index = index
        self._reranker = reranker

    def _get_engine(self):
        if not self._index:
            print("### No index found...")
            return None

        DEFAULT_TEXT_QA_PROMPT_TMPL = (
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "You are an experienced architect specializing in Velux products (building and construction products, TODO(pg)...)."
            "You will answer in Professional architectural and building and construction products Language."
            "Keep your answers short and always deliver only what was asked."
            "Always quote the specific regulation name, paragraph, or norm depending on the case."
            "You should use professional language and have a deep understanding of the relevant laws and guidelines in the field of architecture and construction."
            "Be as descriptive as possible. Always make sure to provide 100% correct information."
            "When responding, avoid giving personal opinions or advice that goes beyond the scope of regulations."
            "In cases of conflicting information, use the most recent regulation by the date of being published."
            "Your responses should be clear, concise, and tailored to the level of understanding of the user, ensuring they receive the most relevant and accurate information."
            "Your goal is to help architects with building regulations so they don't get rejected by the building inspectorate."
            "Query: {query_str}\n"
            "Answer: "
        )
        DEFAULT_TEXT_QA_PROMPT = PromptTemplate(
            DEFAULT_TEXT_QA_PROMPT_TMPL, prompt_type=PromptType.QUESTION_ANSWER
        )

        return self._index.as_chat_engine(
            chat_mode=ChatMode.CONTEXT,
            similarity_top_k=10,
            node_postprocessors=[self._reranker],
            text_qa_template=DEFAULT_TEXT_QA_PROMPT,
            stream=True,
            verbose=True,
        )
        # return self._index.as_query_engine(
        #     text_qa_template=DEFAULT_TEXT_QA_PROMPT, stream=True, verbose=True
        # )

    def _format_chat_history(self, chat_history):
        return [
            ChatMessage(
                role=(
                    MessageRole.USER
                    if isinstance(message, HumanMessage)
                    else (
                        MessageRole.ASSISTANT
                        if isinstance(message, AIMessage)
                        else (
                            MessageRole.SYSTEM
                            if isinstance(message, SystemMessage)
                            else MessageRole.MODEL
                        )
                    )
                ),
                content=message.content,
            )
            for message in chat_history
        ]

    async def generate_stream(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> AsyncIterable:
        print(f"####### Calling generate_stream with question: {question} #######")
        chat_engine = self._get_engine()
        if not chat_engine:
            raise ValueError("No chat engine found")
        transformed_history, streamed_chat_history = (
            self.initialize_streamed_chat_history(chat_id, question)
        )
        print(f"####### transformed_history: {transformed_history} #######")
        llama_index_transformed_history = self._format_chat_history(transformed_history)

        response_tokens = []
        # response = await chat_engine.astream_chat(
        #     message=question.question,
        #     chat_history=llama_index_transformed_history,
        # )
        response = chat_engine.stream_chat(
            message=question.question,
            chat_history=llama_index_transformed_history,
        )
        for chunk in response.response_gen:
            print(chunk)
            response_tokens.append(chunk)
            streamed_chat_history.assistant = chunk
            yield f"data: {json.dumps(streamed_chat_history.dict())}"
        # response = await chat_engine.aquery(
        #     question.question,
        # )
        # streamed_chat_history.assistant = str(response)
        # yield f"data: {json.dumps(streamed_chat_history.dict())}"

        # self.save_answer(question, str(response), streamed_chat_history, save_answer)
        self.save_answer(question, response_tokens, streamed_chat_history, save_answer)
