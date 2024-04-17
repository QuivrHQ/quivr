import os
import json
from typing import AsyncIterable
from uuid import UUID

from llama_index.core import (
    Settings,
    VectorStoreIndex,
    SimpleDirectoryReader,
    load_index_from_storage,
    StorageContext,
)
from llama_index.core.node_parser import MarkdownElementNodeParser

from llama_index.core.llms import ChatMessage
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

current_directory = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.join(current_directory, "luccid-data/Documents")

embed_model = OpenAIEmbedding(model="text-embedding-3-small")
llm = OpenAI(model="gpt-4-turbo-preview")

Settings.llm = llm
Settings.embed_model = embed_model


class LlamaIndexBrain:
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

        # self._vector_store = RedisVectorStore(
        #     index_name="redis_vectore_store",
        #     index_prefix="vector_store",
        #     redis_url="redis://redis:6379",
        # )
        # self._ingestion_cache = IngestionCache(
        #     cache=RedisCache.from_host_and_port("redis", 6379),
        #     collection="redis_cache",
        # )
        # self._ingestion_pipeline = IngestionPipeline(
        #     transformations=[
        #         MarkdownElementNodeParser(),
        #         embed_model,
        #     ],
        #     docstore=RedisDocumentStore.from_host_and_port(
        #         "localhost", 6379, namespace="document_store"
        #     ),
        #     vector_store=self._vector_store,
        #     cache=self._ingestion_cache,
        #     docstore_strategy=DocstoreStrategy.UPSERTS,
        # )
        # self._index = VectorStoreIndex.from_vector_store(
        #     self._vector_store, embed_model=embed_model
        # )
        try:
            self._storage_context = StorageContext.from_defaults(
                persist_dir=os.path.join(current_directory, "index-data")
            )
            self._index = load_index_from_storage(
                storage_context=self._storage_context, index_id="vector_index"
            )
        except ValueError as e:
            if (
                e
                == "No index in storage context, check if you specified the right persist_dir."
            ):
                print(e)
                # docs = self._load_data(folder_name="Serbia", recursive=True)
                # cls._parse_nodes(docs)
            else:
                print(e)
                self._index = None
                # raise e
        except FileNotFoundError as e:
            print(e)
            # docs = self._load_data(folder_name="Serbia", recursive=True)
            # cls._parse_nodes(docs)

    @classmethod
    def _load_data(cls, folder_name: str, recursive: bool = False):
        # credentials_path = os.path.join(
        #     current_directory, "luccid-app-llamaindex-google-readers.json"
        # )
        # print(f"####### PG ####### credentials_path: {credentials_path}")
        # loader = GoogleDriveReader(credentials_path=credentials_path)
        # docs = loader.load_data(
        #     folder_id=folder_id,
        #     query_string="name contains 'corrected.md'",
        #     # TODO(pg): do a PR to add recursive to the GDrive loader
        #     # recursive=recursive
        # )
        # for doc in docs:
        #     doc.id_ = doc.metadata["file_name"]
        reader = SimpleDirectoryReader(
            input_dir=os.path.join(data_directory, folder_name)
        )
        docs = reader.load_data()

        return docs

    @classmethod
    def _parse_nodes(cls, folder_name, docs):
        node_parser = MarkdownElementNodeParser(llm=llm)
        nodes = node_parser.get_nodes_from_documents(docs)
        base_nodes, objects = node_parser.get_nodes_and_objects(nodes)
        index = VectorStoreIndex(nodes=base_nodes + objects)
        index.set_index_id("vector_index")
        index.storage_context.persist(
            os.path.join(data_directory, folder_name, "index-data")
        )
        print(f"Ingested {len(nodes)} Nodes")

    def _get_engine(self):
        if not self._index:
            return None
            # docs = self._load_data(folder_name="Serbia", recursive=True)
            # nodes = self._ingestion_pipeline.run(show_progress=True, documents=docs)

        return self._index.as_chat_engine()

    def _format_chat_history(self, chat_history):
        return [
            ChatMessage(role=message.role, content=message.content)
            for message in chat_history
        ]


if __name__ == "__main__":
    # folder_name = "Serbia"
    folder_name = "Manufacturers/Velux-Serbia"
    # folder_name = "Germany/Bundesland-Berlin"
    try:
        storage_context = StorageContext.from_defaults(
            persist_dir=os.path.join(current_directory, folder_name, "index-data")
        )
    except ValueError as e:
        if (
            e
            == "No index in storage context, check if you specified the right persist_dir."
        ):
            docs = LlamaIndexBrain._load_data(folder_name=folder_name, recursive=True)
            LlamaIndexBrain._parse_nodes(folder_name=folder_name, docs=docs)
        else:
            print(e)
            # raise e
    except FileNotFoundError as e:
        print(f"### {e}")
        docs = LlamaIndexBrain._load_data(folder_name=folder_name, recursive=True)
        LlamaIndexBrain._parse_nodes(folder_name=folder_name, docs=docs)
