from quivr_core.rag.langgraph.state import AgentState
from langgraph.types import Send
from typing import List
import asyncio
from quivr_core.rag.utils import collect_tools
from quivr_core.rag.prompts import TemplatePromptName, custom_prompts
from quivr_core.rag.utils import combine_documents
from quivr_core.rag.langgraph.state import TasksCompletion
from quivr_core.llm_tools.llm_tools import LLMToolFactory


async def tool_routing(self, state: AgentState):
    tasks = state["tasks"]
    if not tasks.has_tasks():
        return [Send("generate_rag", state)]

    validated_tools, _ = collect_tools(self.retrieval_config.workflow_config)

    async_jobs = []
    for task_id in tasks.ids:
        input = {
            "chat_history": state["chat_history"].to_list(),
            "tasks": tasks(task_id).definition,
            "context": combine_documents(tasks(task_id).docs),
            "activated_tools": validated_tools,
        }

        msg = custom_prompts[TemplatePromptName.TOOL_ROUTING_PROMPT].format(**input)
        async_jobs.append(
            (self.ainvoke_structured_output(msg, TasksCompletion), task_id)
        )

    responses: List[TasksCompletion] = (
        await asyncio.gather(*(jobs[0] for jobs in async_jobs)) if async_jobs else []
    )
    task_ids = [jobs[1] for jobs in async_jobs] if async_jobs else []

    for response, task_id in zip(responses, task_ids, strict=False):
        tasks.set_completion(task_id, response.is_task_completable)
        if not response.is_task_completable and response.tool:
            tasks.set_tool(task_id, response.tool)

    send_list: List[Send] = []

    payload = {**state, "tasks": tasks}

    if tasks.has_non_completable_tasks():
        send_list.append(Send("run_tool", payload))
    else:
        send_list.append(Send("generate_rag", payload))

    return send_list


async def run_tool(self, state: AgentState) -> AgentState:
    # if tool not in [
    #     t.name for t in self.retrieval_config.workflow_config.activated_tools
    # ]:
    #     raise ValueError(f"Tool {tool} not activated")

    tasks = state["tasks"]

    # Prepare the async tasks for all questions
    async_jobs = []
    for task_id in tasks.ids:
        if not tasks(task_id).is_completable() and tasks(task_id).has_tool():
            tool = tasks(task_id).tool
            tool_wrapper = LLMToolFactory.create_tool(tool, {})
            formatted_input = tool_wrapper.format_input(tasks(task_id).definition)
            async_jobs.append((tool_wrapper.tool.ainvoke(formatted_input), task_id))

    # Gather all the responses asynchronously
    responses = (
        await asyncio.gather(*(jobs[0] for jobs in async_jobs)) if async_jobs else []
    )
    task_ids = [jobs[1] for jobs in async_jobs] if async_jobs else []

    for response, task_id in zip(responses, task_ids, strict=False):
        _docs = tool_wrapper.format_output(response)
        _docs = self.filter_chunks_by_relevance(_docs)
        tasks.set_docs(task_id, _docs)

    return {**state, "tasks": tasks}
