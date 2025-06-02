from typing import List, Dict, Any, Tuple
from quivr_core.rag.langgraph.state import AgentState, UpdatedPromptAndTools
from langchain_core.prompts import BasePromptTemplate
from langchain_core.documents import Document
from quivr_core.rag.prompts import TemplatePromptName, custom_prompts
from quivr_core.rag.utils import combine_documents
import logging

logger = logging.getLogger(__name__)


def update_active_tools(self, updated_prompt_and_tools: UpdatedPromptAndTools):
    if updated_prompt_and_tools.tools_to_activate:
        for tool in updated_prompt_and_tools.tools_to_activate:
            for validated_tool in self.retrieval_config.workflow_config.validated_tools:
                if tool == validated_tool.name:
                    self.retrieval_config.workflow_config.activated_tools.append(
                        validated_tool
                    )

    if updated_prompt_and_tools.tools_to_deactivate:
        for tool in updated_prompt_and_tools.tools_to_deactivate:
            for activated_tool in self.retrieval_config.workflow_config.activated_tools:
                if tool == activated_tool.name:
                    self.retrieval_config.workflow_config.activated_tools.remove(
                        activated_tool
                    )


def filter_chunks_by_relevance(self, chunks: List[Document], **kwargs):
    config = self.retrieval_config.reranker_config
    relevance_score_threshold = kwargs.get(
        "relevance_score_threshold", config.relevance_score_threshold
    )

    if relevance_score_threshold is None:
        return chunks

    filtered_chunks = []
    for chunk in chunks:
        if config.relevance_score_key not in chunk.metadata:
            logger.warning(
                f"Relevance score key {config.relevance_score_key} not found in metadata, cannot filter chunks by relevance"
            )
            filtered_chunks.append(chunk)
        elif chunk.metadata[config.relevance_score_key] >= relevance_score_threshold:
            filtered_chunks.append(chunk)

    return filtered_chunks


def _sort_docs_by_relevance(self, docs: List[Document]) -> List[Document]:
    return sorted(
        docs,
        key=lambda x: x.metadata[
            self.retrieval_config.reranker_config.relevance_score_key
        ],
        reverse=True,
    )


def get_rag_context_length(self, state: AgentState, docs: List[Document]) -> int:
    final_inputs = self._build_rag_prompt_inputs(state, docs)
    msg = custom_prompts[TemplatePromptName.RAG_ANSWER_PROMPT].format(**final_inputs)
    return self.llm_endpoint.count_tokens(msg)


def reduce_rag_context(
    self,
    state: AgentState,
    inputs: Dict[str, Any],
    prompt: BasePromptTemplate,
    max_context_tokens: int | None = None,
) -> Tuple[AgentState, Dict[str, Any]]:
    MAX_ITERATIONS = 20
    SECURITY_FACTOR = 0.85
    iteration = 0

    tasks = state["tasks"] if "tasks" in state else None
    docs = tasks.docs if tasks else []
    msg = prompt.format(**inputs)
    n = self.llm_endpoint.count_tokens(msg)

    max_context_tokens = (
        max_context_tokens
        if max_context_tokens
        else self.retrieval_config.llm_config.max_context_tokens
    )

    # Get token counts for each doc in each task
    if tasks:
        task_token_counts = {}
        for task_id in tasks.ids:
            doc_tokens = [
                self.llm_endpoint.count_tokens(doc.page_content)
                for doc in tasks(task_id).docs
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
        n = self.llm_endpoint.count_tokens(msg)

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
