from quivr_core.rag.langgraph.state import AgentState
from quivr_core.rag.prompts import TemplatePromptName, custom_prompts
from quivr_core.rag.utils import collect_tools
from quivr_core.rag.langgraph.state import (
    SplittedInput,
    UpdatedPromptAndTools,
    UserTasks,
)
from langgraph.types import Send
from typing import List
import openai
from uuid import uuid4
from quivr_core.rag.entities.chat import ChatHistory
import asyncio


def routing(self, state: AgentState) -> List[Send]:
    """
    The routing function for the RAG model.

    Args:
        state (AgentState): The current state of the agent.

    Returns:
        dict: The next state of the agent.
    """

    msg = custom_prompts[TemplatePromptName.SPLIT_PROMPT].format(
        user_input=state["messages"][0].content,
    )

    response: SplittedInput

    try:
        structured_llm = self.llm_endpoint._llm.with_structured_output(
            SplittedInput, method="json_schema"
        )
        response = structured_llm.invoke(msg)

    except openai.BadRequestError:
        structured_llm = self.llm_endpoint._llm.with_structured_output(SplittedInput)
        response = structured_llm.invoke(msg)

    send_list: List[Send] = []

    instructions = (
        response.instructions if response.instructions else self.retrieval_config.prompt
    )

    if instructions:
        send_list.append(Send("edit_system_prompt", {"instructions": instructions}))
    elif response.task_list:
        chat_history = state["chat_history"]
        send_list.append(
            Send(
                "filter_history",
                {
                    "chat_history": chat_history,
                    "tasks": UserTasks(response.task_list),
                },
            )
        )

    return send_list


def routing_split(self, state: AgentState):
    response: SplittedInput = self.invoke_structured_output(
        custom_prompts[TemplatePromptName.SPLIT_PROMPT].format(
            chat_history=state["chat_history"].to_list(),
            user_input=state["messages"][0].content,
        ),
        SplittedInput,
    )

    instructions = response.instructions or self.retrieval_config.prompt
    tasks = UserTasks(response.task_list) if response.task_list else None

    if instructions:
        return [
            Send(
                "edit_system_prompt",
                {**state, "instructions": instructions, "tasks": tasks},
            )
        ]
    elif tasks:
        return [Send("filter_history", {**state, "tasks": tasks})]

    return []


def edit_system_prompt(self, state: AgentState) -> AgentState:
    user_instruction = state["instructions"]
    prompt = self.retrieval_config.prompt
    available_tools, activated_tools = collect_tools(
        self.retrieval_config.workflow_config
    )
    inputs = {
        "instruction": user_instruction,
        "system_prompt": prompt if prompt else "",
        "available_tools": available_tools,
        "activated_tools": activated_tools,
    }

    msg = custom_prompts[TemplatePromptName.UPDATE_PROMPT].format(**inputs)

    response: UpdatedPromptAndTools = self.invoke_structured_output(
        msg, UpdatedPromptAndTools
    )

    self.update_active_tools(response)
    self.retrieval_config.prompt = response.prompt

    reasoning = [response.prompt_reasoning] if response.prompt_reasoning else []
    reasoning += [response.tools_reasoning] if response.tools_reasoning else []

    return {**state, "messages": [], "reasoning": reasoning}


def filter_history(self, state: AgentState) -> AgentState:
    """
    Filter out the chat history to only include the messages that are relevant to the current question

    Takes in a chat_history= [HumanMessage(content='Qui est Chloé ? '),
    AIMessage(content="Chloé est une salariée travaillant pour l'entreprise Quivr en tant qu'AI Engineer,
    sous la direction de son supérieur hiérarchique, Stanislas Girard."),
    HumanMessage(content='Dis moi en plus sur elle'), AIMessage(content=''),
    HumanMessage(content='Dis moi en plus sur elle'),
    AIMessage(content="Désolé, je n'ai pas d'autres informations sur Chloé à partir des fichiers fournis.")]
    Returns a filtered chat_history with in priority: first max_tokens, then max_history where a Human message and an AI message count as one pair
    a token is 4 characters
    """

    chat_history = state["chat_history"]
    total_tokens = 0
    total_pairs = 0
    _chat_id = uuid4()
    _chat_history = ChatHistory(chat_id=_chat_id, brain_id=chat_history.brain_id)
    for human_message, ai_message in reversed(list(chat_history.iter_pairs())):
        # TODO: replace with tiktoken
        message_tokens = self.llm_endpoint.count_tokens(
            human_message.content
        ) + self.llm_endpoint.count_tokens(ai_message.content)

        if (
            total_tokens + message_tokens
            > self.retrieval_config.llm_config.max_context_tokens
            or total_pairs >= self.retrieval_config.max_history
        ):
            break
        _chat_history.append(human_message)
        _chat_history.append(ai_message)
        total_tokens += message_tokens
        total_pairs += 1

    return {**state, "chat_history": _chat_history}


async def rewrite(self, state: AgentState) -> AgentState:
    """
    Transform the query to produce a better question.

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with re-phrased question
    """

    if "tasks" in state and state["tasks"]:
        tasks = state["tasks"]
    else:
        tasks = UserTasks([state["messages"][0].content])

    # Prepare the async tasks for all user tsks
    async_jobs = []
    for task_id in tasks.ids:
        msg = custom_prompts[TemplatePromptName.CONDENSE_TASK_PROMPT].format(
            chat_history=state["chat_history"].to_list(),
            task=tasks(task_id).definition,
        )

        model = self.llm_endpoint._llm
        # Asynchronously invoke the model for each question
        async_jobs.append((model.ainvoke(msg), task_id))

    # Gather all the responses asynchronously
    responses = (
        await asyncio.gather(*(jobs[0] for jobs in async_jobs)) if async_jobs else []
    )
    task_ids = [jobs[1] for jobs in async_jobs] if async_jobs else []

    # Replace each question with its condensed version
    for response, task_id in zip(responses, task_ids, strict=False):
        tasks.set_definition(task_id, response.content)

    return {**state, "tasks": tasks}
