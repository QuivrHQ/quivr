from typing import Dict, Any
from langchain.memory import ConversationBufferMemory

class AnswerConversationBufferMemory(ConversationBufferMemory):
    """ref https://github.com/hwchase17/langchain/issues/5630#issuecomment-1574222564"""
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        return super(AnswerConversationBufferMemory, self).save_context(
            inputs, {'response': outputs['answer']})
    