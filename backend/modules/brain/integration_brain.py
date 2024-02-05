from pydantic import BaseModel

from backend.modules.brain.qa_interface import QAInterface


class IntegrationBrain(QAInterface, BaseModel):
    """Integration brain class use to redirect the user to the correct brain

    Args:
        QAInterface (_type_): Has the Question methods
        BaseModel (_type_): _description_
    """

    def __init__(self):
        super().__init__()
    