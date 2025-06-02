from quivr_core.rag.langgraph.state import AgentState, UserTasks
from langchain.retrievers import ContextualCompressionRetriever
import asyncio
import logging
from collections import OrderedDict
from typing import Dict, Any

logger = logging.getLogger(__name__)


async def retrieve(self, state: AgentState) -> AgentState:
    """
    Retrieve relevent chunks

    Args:
        state (messages): The current state

    Returns:
        dict: The retrieved chunks
    """
    if "tasks" in state:
        tasks = state["tasks"]
    else:
        tasks = UserTasks([state["messages"][0].content])

    if not tasks.has_tasks():
        return {**state}

    _filter = state.get("_filter", None)

    kwargs = {
        "search_kwargs": {
            "k": self.retrieval_config.k,
            "filter": _filter,  # Add your desired filter here
        }
    }  # type: ignore
    base_retriever = self.get_retriever(**kwargs)

    kwargs = {"top_n": self.retrieval_config.reranker_config.top_n}  # type: ignore
    reranker = self.get_reranker(**kwargs)

    compression_retriever = ContextualCompressionRetriever(
        base_compressor=reranker, base_retriever=base_retriever
    )

    # Prepare the async tasks for all questions
    async_jobs = []
    for task_id in tasks.ids:
        # Create a tuple of the retrieval task and task_id
        async_jobs.append(
            (compression_retriever.ainvoke(tasks(task_id).definition), task_id)
        )

    # Gather all the responses asynchronously
    responses = (
        await asyncio.gather(*(task[0] for task in async_jobs)) if async_jobs else []
    )
    task_ids = [task[1] for task in async_jobs] if async_jobs else []

    # Process responses and associate docs with tasks
    for response, task_id in zip(responses, task_ids, strict=False):
        _docs = self.filter_chunks_by_relevance(response)
        tasks.set_docs(task_id, _docs)  # Associate docs with the specific task

    return {**state, "tasks": tasks}


async def dynamic_retrieve(self, state: AgentState) -> AgentState:
    """
    Retrieve relevent chunks

    Args:
        state (messages): The current state

    Returns:
        dict: The retrieved chunks
    """

    MAX_ITERATIONS = 3

    if "tasks" in state:
        tasks = state["tasks"]
    else:
        tasks = UserTasks([state["messages"][0].content])

    if not tasks or not tasks.has_tasks():
        return {**state}

    k = self.retrieval_config.k
    top_n = self.retrieval_config.reranker_config.top_n
    number_of_relevant_chunks = top_n
    i = 1

    while number_of_relevant_chunks == top_n and i <= MAX_ITERATIONS:
        top_n = self.retrieval_config.reranker_config.top_n * i
        kwargs = {"top_n": top_n}
        reranker = self.get_reranker(**kwargs)

        k = max([top_n * 2, self.retrieval_config.k])
        kwargs = {"search_kwargs": {"k": k}}  # type: ignore
        base_retriever = self.get_retriever(**kwargs)

        if i > 1:
            logging.info(
                f"Increasing top_n to {top_n} and k to {k} to retrieve more relevant chunks"
            )

        compression_retriever = ContextualCompressionRetriever(
            base_compressor=reranker, base_retriever=base_retriever
        )

        # Prepare the async tasks for all questions
        async_jobs = []
        for task_id in tasks.ids:
            # Asynchronously invoke the model for each question
            async_jobs.append(
                (compression_retriever.ainvoke(tasks(task_id).definition), task_id)
            )

        # Gather all the responses asynchronously
        responses = (
            await asyncio.gather(*(jobs[0] for jobs in async_jobs))
            if async_jobs
            else []
        )
        task_ids = [jobs[1] for jobs in async_jobs] if async_jobs else []

        _n = []
        for response, task_id in zip(responses, task_ids, strict=False):
            _docs = self.filter_chunks_by_relevance(response)
            _n.append(len(_docs))
            tasks.set_docs(task_id, _docs)

        docs = tasks.docs
        if not docs:
            break

        context_length = self.get_rag_context_length(state, docs)
        if context_length >= self.retrieval_config.llm_config.max_context_tokens:
            logging.warning(
                f"The context length is {context_length} which is greater than "
                f"the max context tokens of {self.retrieval_config.llm_config.max_context_tokens}"
            )
            break

        number_of_relevant_chunks = max(_n)
        i += 1

    return {**state, "tasks": tasks}


async def retrieve_full_documents_context(self, state: AgentState) -> AgentState:
    if "tasks" in state:
        tasks = state["tasks"]
    else:
        tasks = UserTasks([state["messages"][0].content])

    if not tasks.has_tasks():
        return {**state}

    docs = tasks.docs if tasks else []

    relevant_knowledge: Dict[str, Dict[str, Any]] = {}
    for doc in docs:
        knowledge_id = doc.metadata["knowledge_id"]
        similarity_score = doc.metadata.get("similarity", 0)
        if knowledge_id in relevant_knowledge:
            relevant_knowledge[knowledge_id]["count"] += 1
            relevant_knowledge[knowledge_id]["max_similarity_score"] = max(
                relevant_knowledge[knowledge_id]["max_similarity_score"],
                similarity_score,
            )
            relevant_knowledge[knowledge_id]["chunk_index"] = max(
                doc.metadata["chunk_index"],
                relevant_knowledge[knowledge_id]["chunk_index"],
            )
        else:
            relevant_knowledge[knowledge_id] = {
                "count": 1,
                "max_similarity_score": similarity_score,
                "chunk_index": doc.metadata["chunk_index"],
            }

    top_n = min(3, len(relevant_knowledge))
    # FIXME: Tweak this to return the most relevant knowledges
    top_knowledge_ids = OrderedDict(
        sorted(
            relevant_knowledge.items(),
            key=lambda x: (
                x[1]["max_similarity_score"],
                x[1]["count"],
            ),
            reverse=True,
        )[:top_n]
    )

    logger.info(f"Top knowledge IDs: {top_knowledge_ids}")

    _docs = []

    assert hasattr(
        self.vector_store, "get_vectors_by_knowledge_id"
    ), "Vector store must have method 'get_vectors_by_knowledge_id', this is an enterprise only feature"

    for knowledge_id in top_knowledge_ids:
        _docs.append(
            await self.vector_store.get_vectors_by_knowledge_id(  # type: ignore
                knowledge_id,
                end_index=relevant_knowledge[knowledge_id]["chunk_index"],
            )
        )

    tasks.set_docs(id=tasks.ids[0], docs=_docs)  # FIXME If multiple IDs is not handled.

    return {**state, "tasks": tasks}
