from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Sequence, TypedDict, Annotated
from langchain_core.callbacks import Callbacks
from langchain_core.documents import BaseDocumentCompressor, Document
from quivr_core.rag.entities.chat import ChatHistory
from langgraph.graph.message import add_messages
from quivr_core.rag.langgraph_framework.task import UserTasks


class TasksCompletion(BaseModel):
    is_task_completable_reasoning: Optional[str] = Field(
        default=None,
        description="The reasoning that leads to identifying whether the user task or question can be completed using the provided context and chat history BEFORE any tool is used.",
    )

    is_task_completable: bool = Field(
        description="Whether the user task or question can be completed using the provided context and chat history BEFORE any tool is used.",
    )

    tool_reasoning: Optional[str] = Field(
        default=None,
        description="The reasoning that leads to identifying the tool that shall be used to complete the task.",
    )
    tool: Optional[str] = Field(
        description="The tool that shall be used to complete the task.",
    )


class FinalAnswer(BaseModel):
    reasoning_answer: str = Field(
        description="The step-by-step reasoning that led to the final answer"
    )
    answer: str = Field(description="The final answer to the user tasks/questions")

    all_tasks_completed: bool = Field(
        description="Whether all tasks/questions have been successfully answered/completed or not. "
        " If the final answer to the user is 'I don't know' or 'I don't have enough information' or 'I'm not sure', "
        " this variable should be 'false'"
    )


class UpdatedPromptAndTools(BaseModel):
    prompt_reasoning: Optional[str] = Field(
        default=None,
        description="The step-by-step reasoning that leads to the updated system prompt",
    )
    prompt: Optional[str] = Field(default=None, description="The updated system prompt")

    tools_reasoning: Optional[str] = Field(
        default=None,
        description="The reasoning that leads to activating and deactivating the tools",
    )
    tools_to_activate: Optional[List[str]] = Field(
        default_factory=list, description="The list of tools to activate"
    )
    tools_to_deactivate: Optional[List[str]] = Field(
        default_factory=list, description="The list of tools to deactivate"
    )


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    reasoning: List[str]
    chat_history: ChatHistory
    files: str
    tasks: UserTasks
    instructions: str
    ticket_metadata: Optional[dict[str, str]]
    user_metadata: Optional[dict[str, str]]
    additional_information: Optional[dict[str, str]]
    tool: str
    guidelines: str
    enforced_system_prompt: str
    _filter: Optional[Dict[str, Any]]
    ticket_history: str


class IdempotentCompressor(BaseDocumentCompressor):
    def compress_documents(
        self,
        documents: Sequence[Document],
        query: str,
        callbacks: Optional[Callbacks] = None,
    ) -> Sequence[Document]:
        """
        A no-op document compressor that simply returns the documents it is given.

        This is a placeholder until a more sophisticated document compression
        algorithm is implemented.
        """
        return documents
