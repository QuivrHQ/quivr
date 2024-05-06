import os

from llama_index.core import (
    Settings,
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
from llama_index.core.node_parser import MarkdownElementNodeParser

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

data_directory = "/home/pascal_gula_luccid_ai/luccid-data/"
folder_name = "Documents/Manufacturers/Velux-UK"
index_data = os.path.join(data_directory, folder_name, "index-data")

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

    @classmethod
    def _load_data(cls, recursive: bool = False):
        reader = SimpleDirectoryReader(
            input_dir=os.path.join(data_directory, folder_name), recursive=recursive
        )
        docs = reader.load_data()

        return docs

    @classmethod
    def _parse_nodes(cls, docs):
        node_parser = MarkdownElementNodeParser(llm=llm)
        nodes = node_parser.get_nodes_from_documents(docs)
        base_nodes, objects = node_parser.get_nodes_and_objects(nodes)
        index = VectorStoreIndex(nodes=base_nodes + objects)
        index.set_index_id("vector_index")
        index.storage_context.persist(index_data)
        print(f"Ingested {len(nodes)} Nodes")


if __name__ == "__main__":
    try:
        storage_context = StorageContext.from_defaults(
            persist_dir=index_data
        )
    except ValueError as e:
        if (
            e
            == "No index in storage context, check if you specified the right persist_dir."
        ):
            docs = LlamaIndexBrain._load_data(recursive=True)
            LlamaIndexBrain._parse_nodes(docs=docs)
        else:
            print(e)
            # raise e
    except FileNotFoundError as e:
        print(f"### {e}")
        docs = LlamaIndexBrain._load_data(recursive=True)
        LlamaIndexBrain._parse_nodes(docs=docs)
