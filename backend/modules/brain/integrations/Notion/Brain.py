from modules.brain.knowledge_brain_qa import KnowledgeBrainQA


class NotionBrain(KnowledgeBrainQA):
    """
    NotionBrain integrates with Notion to provide knowledge-based responses.
    It leverages data stored in Notion to answer user queries.

    Attributes:
        **kwargs: Arbitrary keyword arguments for KnowledgeBrainQA initialization.
    """

    def __init__(
        self,
        **kwargs,
    ):
        """
        Initializes the NotionBrain with the given arguments.

        Args:
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(
            **kwargs,
        )
