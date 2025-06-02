from typing import List
from langchain_core.prompts import BasePromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.documents import Document
from langchain_core.utils import format_dict
import datetime
from quivr_core.rag.langgraph.state import AgentState
from quivr_core.rag.prompts import TemplatePromptName, custom_prompts


def generate_zendesk_rag(self, state: AgentState) -> AgentState:
    tasks = state["tasks"]
    docs: List[Document] = tasks.docs if tasks else []
    messages = state["messages"]
    user_task = messages[0].content
    prompt_template: BasePromptTemplate = custom_prompts[
        TemplatePromptName.ZENDESK_TEMPLATE_PROMPT
    ]

    ticket_metadata = state["ticket_metadata"] or {}
    user_metadata = state["user_metadata"] or {}
    ticket_history = state.get("ticket_history", "")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    inputs = {
        "similar_tickets": "\n".join([doc.page_content for doc in docs]),
        "ticket_metadata": format_dict(ticket_metadata),
        "user_metadata": format_dict(user_metadata),
        "client_query": user_task,
        "ticket_history": ticket_history,
        "current_time": current_time,
    }
    required_variables = prompt_template.input_variables
    for variable in required_variables:
        if variable not in inputs:
            inputs[variable] = state.get(variable, "")

    msg = prompt_template.format_prompt(**inputs)
    llm = self.bind_tools_to_llm(self.generate_zendesk_rag.__name__)

    response = llm.invoke(msg)

    return {**state, "messages": [response]}


def generate_rag(self, state: AgentState) -> AgentState:
    tasks = state["tasks"]
    docs = tasks.docs if tasks else []
    inputs = self._build_rag_prompt_inputs(state, docs)
    prompt = custom_prompts[TemplatePromptName.RAG_ANSWER_PROMPT]
    state, inputs = self.reduce_rag_context(state, inputs, prompt)
    msg = prompt.format(**inputs)
    llm = self.bind_tools_to_llm(self.generate_rag.__name__)
    response = llm.invoke(msg)

    return {**state, "messages": [response]}


def generate_chat_llm(self, state: AgentState) -> AgentState:
    """
    Generate answer

    Args:
        state (messages): The current state

    Returns:
        dict: The updated state with re-phrased question
    """
    messages = state["messages"]

    # Check if there is a system message in messages
    system_message = None
    user_message = None

    for msg in messages:
        if isinstance(msg, SystemMessage):
            system_message = str(msg.content)
        elif isinstance(msg, HumanMessage):
            user_message = str(msg.content)

    user_task = (
        user_message if user_message else (messages[0].content if messages else "")
    )

    # Prompt
    prompt = self.retrieval_config.prompt

    final_inputs = {}
    final_inputs["task"] = user_task
    final_inputs["custom_instructions"] = prompt if prompt else "None"
    final_inputs["chat_history"] = state["chat_history"].to_list()

    # LLM
    llm = self.llm_endpoint._llm

    prompt = custom_prompts[TemplatePromptName.CHAT_LLM_PROMPT]
    state, reduced_inputs = self.reduce_rag_context(
        state, final_inputs, system_message if system_message else prompt
    )
    CHAT_LLM_PROMPT = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=str(system_message)),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content=str(user_message)),
        ]
    )
    # Run
    chat_llm_prompt = CHAT_LLM_PROMPT.invoke(
        {"chat_history": final_inputs["chat_history"]}
    )
    response = llm.invoke(chat_llm_prompt)
    return {**state, "messages": [response]}
