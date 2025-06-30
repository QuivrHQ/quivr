from typing import Callable, List, Dict, Any, Tuple, TypedDict
from quivr_core.rag.entities.config import WorkflowConfig
from quivr_core.rag.langgraph_framework.state import AgentState, UpdatedPromptAndTools
from langchain_core.prompts import BasePromptTemplate
from langchain_core.documents import Document
from quivr_core.rag.prompt.registry import get_prompt
from quivr_core.rag.utils import combine_documents
import logging

logger = logging.getLogger(__name__)


def update_active_tools(
    workflow_config: WorkflowConfig, updated_prompt_and_tools: UpdatedPromptAndTools
):
    if updated_prompt_and_tools.tools_to_activate:
        for tool in updated_prompt_and_tools.tools_to_activate:
            for validated_tool in workflow_config.validated_tools:
                if tool == validated_tool.name:
                    workflow_config.activated_tools.append(validated_tool)

    if updated_prompt_and_tools.tools_to_deactivate:
        for tool in updated_prompt_and_tools.tools_to_deactivate:
            for activated_tool in workflow_config.activated_tools:
                if tool == activated_tool.name:
                    workflow_config.activated_tools.remove(activated_tool)


def get_rag_context_length(self, state: AgentState, docs: List[Document]) -> int:
    final_inputs = self._build_rag_prompt_inputs(state, docs)
    msg = get_prompt("rag_answer").format(**final_inputs)
    return self.llm_endpoint.count_tokens(msg)


def reduce_rag_context(
    state: Dict[str, Any],
    inputs: Dict[str, Any],
    prompt: BasePromptTemplate,
    count_tokens_fn: Callable[[str], int],
    max_context_tokens: int,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Reduce the context length of the RAG context by removing the least relevant documents.
    """
    MAX_ITERATIONS = 20
    SECURITY_FACTOR = 0.85
    iteration = 0

    tasks = state["tasks"] if "tasks" in state else None
    docs = tasks.docs if tasks else []
    msg = prompt.format(**inputs)
    n = count_tokens_fn(msg)

    class TaskTokenCount(TypedDict):
        docs: List[int]
        total: int

    # Get token counts for each doc in each task
    task_token_counts: Dict[str, TaskTokenCount] = {}
    if tasks:
        for task_id in tasks.ids:
            doc_tokens = [
                count_tokens_fn(doc.page_content) for doc in tasks(task_id).docs
            ]
            task_token_counts[task_id] = {
                "docs": doc_tokens,
                "total": sum(doc_tokens),
            }

    while n > max_context_tokens * SECURITY_FACTOR:
        chat_history = inputs["chat_history"] if "chat_history" in inputs else []

        if len(chat_history) > 0:
            inputs["chat_history"] = chat_history[2:]
        elif tasks:
            longest_task_id = max(
                task_token_counts.items(), key=lambda x: x[1]["total"]
            )[0]

            # Remove last doc from that task
            if task_token_counts[longest_task_id]["docs"]:
                removed_tokens = task_token_counts[longest_task_id]["docs"].pop()
                task_token_counts[longest_task_id]["total"] -= removed_tokens
                tasks.set_docs(longest_task_id, tasks(longest_task_id).docs[:-1])
        else:
            logging.warning(
                f"Not enough context to reduce. The context length is {n} "
                f"which is greater than the max context tokens of {max_context_tokens}"
            )
            break

        docs = tasks.docs if tasks else []
        inputs["context"] = combine_documents(docs)

        msg = prompt.format(**inputs)
        n = count_tokens_fn(msg)

        iteration += 1
        if iteration > MAX_ITERATIONS:
            logging.warning(
                f"Attained the maximum number of iterations ({MAX_ITERATIONS})"
            )
            break

    return {**state, "tasks": tasks}, inputs


def bind_tools_to_llm(self, node_name: str):
    if self.llm_endpoint.supports_func_calling():
        tools = self.retrieval_config.workflow_config.get_node_tools(node_name)
        if tools:  # Only bind tools if there are any available
            return self.llm_endpoint._llm.bind_tools(tools, tool_choice="any")
    return self.llm_endpoint._llm
