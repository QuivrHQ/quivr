from modules.brain.knowledge_brain_qa import KnowledgeBrainQA


class LlamaIndexBrain(KnowledgeBrainQA):
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
