import logging
from operator import add
from typing import (
    Annotated,
    AsyncGenerator,
    List,
    Optional,
    Sequence,
    Tuple,
    TypedDict,
    Dict,
    Any,
)
from uuid import uuid4
import asyncio
from copy import deepcopy

# TODO(@aminediro): this is the only dependency to langchain package, we should remove it
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_community.document_compressors import JinaRerank
from langchain_core.callbacks import Callbacks
from langchain_core.documents import BaseDocumentCompressor, Document
from langchain_core.messages import BaseMessage
from langchain_core.messages.ai import AIMessageChunk
from langchain_core.vectorstores import VectorStore
from langchain_core.prompts.base import BasePromptTemplate
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.types import Send


from pydantic import BaseModel, Field
import openai

from quivr_core.chat import ChatHistory
from quivr_core.config import DefaultRerankers, RetrievalConfig
from quivr_core.llm import LLMEndpoint
from quivr_core.llm_tools.llm_tools import LLMToolFactory
from quivr_core.models import (
    ParsedRAGChunkResponse,
    QuivrKnowledge,
)
from quivr_core.prompts import custom_prompts
from quivr_core.utils import (
    collect_tools,
    combine_documents,
    format_file_list,
    get_chunk_metadata,
    parse_chunk_response,
)

logger = logging.getLogger("quivr_core")


class UserIntent(BaseModel):
    intent: str = Field(description="The user intent")


class SplittedInput(BaseModel):
    instructions: Optional[str] = Field(
        default=None, description="The instructions to the system"
    )
    tasks: Optional[List[str]] = Field(
        default=None,
        description="The list of standalone, self-contained tasks or questions.",
    )


class TasksCompletion(BaseModel):
    completable_tasks: Optional[List[str]] = Field(
        default=None,
        description="The user tasks or questions that can be completed using the provided context and chat history.",
    )
    non_completable_tasks: Optional[List[str]] = Field(
        default=None,
        description="The user tasks or questions that need a web search to be completed.",
    )


class UpdatedPromptAndTools(BaseModel):
    prompt: Optional[str] = Field(default=None, description="The updated system prompt")
    prompt_reasoning: Optional[str] = Field(
        default=None, description="The reasoning that led to the updated system prompt"
    )

    tools_to_activate: Optional[List[str]] = Field(
        default=None, description="The list of tools to activate"
    )
    tools_to_deactivate: Optional[List[str]] = Field(
        default=None, description="The list of tools to deactivate"
    )
    reasoning_tools: Optional[str] = Field(
        default=None,
        description="The reasoning that led to the tools to activate and deactivate",
    )


class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]
    reasoning: Annotated[List[str], add]
    chat_history: ChatHistory
    docs: list[Document]
    files: str
    tasks: List[str]
    instructions: str


class InstructionsState(TypedDict):
    instructions: str


class QuestionsState(TypedDict):
    individual_chat_history: ChatHistory
    question: str


class GenerateInputState(AgentState, QuestionsState):
    pass


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


class QuivrQARAGLangGraph:
    def __init__(
        self,
        *,
        retrieval_config: RetrievalConfig,
        llm: LLMEndpoint,
        vector_store: VectorStore | None = None,
    ):
        """
        Construct a QuivrQARAGLangGraph object.

        Args:
            retrieval_config (RetrievalConfig): The configuration for the RAG model.
            llm (LLMEndpoint): The LLM to use for generating text.
            vector_store (VectorStore): The vector store to use for storing and retrieving documents.
            reranker (BaseDocumentCompressor | None): The document compressor to use for re-ranking documents. Defaults to IdempotentCompressor if not provided.
        """
        self.retrieval_config = retrieval_config
        self.vector_store = vector_store
        self.llm_endpoint = llm

        self.graph = None

    def get_reranker(self, **kwargs):
        # Extract the reranker configuration from self
        config = self.retrieval_config.reranker_config

        # Allow kwargs to override specific config values
        supplier = kwargs.pop("supplier", config.supplier)
        model = kwargs.pop("model", config.model)
        top_n = kwargs.pop("top_n", config.top_n)
        api_key = kwargs.pop("api_key", config.api_key)

        if supplier == DefaultRerankers.COHERE:
            reranker = CohereRerank(
                model=model, top_n=top_n, cohere_api_key=api_key, **kwargs
            )
        elif supplier == DefaultRerankers.JINA:
            reranker = JinaRerank(
                model=model, top_n=top_n, jina_api_key=api_key, **kwargs
            )
        else:
            reranker = IdempotentCompressor()

        return reranker

    def get_retriever(self, **kwargs):
        """
        Returns a retriever that can retrieve documents from the vector store.

        Returns:
            VectorStoreRetriever: The retriever.
        """
        if self.vector_store:
            retriever = self.vector_store.as_retriever(**kwargs)
        else:
            raise ValueError("No vector store provided")

        return retriever

    # def routing(self, state: AgentState) -> str:
    #     """
    #     The routing function for the RAG model.

    #     Args:
    #         state (AgentState): The current state of the agent.

    #     Returns:
    #         dict: The next state of the agent.
    #     """

    #     msg = custom_prompts.USER_INTENT_PROMPT.format(
    #         question=state["messages"][0].content,
    #     )

    #     try:
    #         structured_llm = self.llm_endpoint._llm.with_structured_output(
    #             UserIntent, method="json_schema"
    #         )
    #         response = structured_llm.invoke(msg)

    #     except openai.BadRequestError:
    #         structured_llm = self.llm_endpoint._llm.with_structured_output(UserIntent)
    #         response = structured_llm.invoke(msg)

    #     return response.intent

    def routing(self, state: AgentState) -> List[Send]:
        """
        The routing function for the RAG model.

        Args:
            state (AgentState): The current state of the agent.

        Returns:
            dict: The next state of the agent.
        """

        msg = custom_prompts.SPLIT_PROMPT.format(
            user_input=state["messages"][0].content,
        )

        try:
            structured_llm = self.llm_endpoint._llm.with_structured_output(
                SplittedInput, method="json_schema"
            )
            response = structured_llm.invoke(msg)

        except openai.BadRequestError:
            structured_llm = self.llm_endpoint._llm.with_structured_output(
                SplittedInput
            )
            response = structured_llm.invoke(msg)

        send_list: List[Send] = []

        instructions = (
            response.instructions
            if response.instructions
            else self.retrieval_config.prompt
        )

        if instructions:
            send_list.append(Send("edit_system_prompt", {"instructions": instructions}))
        elif response.tasks:
            chat_history = state["chat_history"]
            send_list.append(
                Send(
                    "filter_history",
                    {"chat_history": chat_history, "tasks": response.tasks},
                )
            )

        return send_list

    def routing_split(self, state: AgentState):
        input = {
            "chat_history": state["chat_history"].to_list(),
            "user_input": state["messages"][0].content,
        }

        msg = custom_prompts.SPLIT_PROMPT.format(**input)

        try:
            structured_llm = self.llm_endpoint._llm.with_structured_output(
                SplittedInput, method="json_schema"
            )
            response = structured_llm.invoke(msg)

        except openai.BadRequestError:
            structured_llm = self.llm_endpoint._llm.with_structured_output(
                SplittedInput
            )
            response = structured_llm.invoke(msg)

        send_list: List[Send] = []
        instructions = (
            response.instructions
            if response.instructions
            else self.retrieval_config.prompt
        )

        if instructions:
            payload = {
                **state,
                "instructions": instructions,
                "tasks": response.tasks if response.tasks else [],
            }
            send_list.append(Send("edit_system_prompt", payload))
        elif response.tasks:
            chat_history = state["chat_history"]
            payload = {
                **state,
                "chat_history": chat_history,
                "tasks": response.tasks,
            }
            send_list.append(Send("filter_history", payload))

        return send_list

    # Here we generate a joke, given a subject
    # def generate_joke(state: JokeState):
    #     prompt = joke_prompt.format(subject=state["subject"])
    #     response = model.with_structured_output(Joke).invoke(prompt)
    #     return {"jokes": [response.joke]}

    # # Here we define the logic to map out over the generated subjects
    # # We will use this an edge in the graph
    # def continue_to_jokes(state: OverallState):
    #     # We will return a list of `Send` objects
    #     # Each `Send` object consists of the name of a node in the graph
    #     # as well as the state to send to that node
    #     return [Send("generate_joke", {"subject": s}) for s in state["subjects"]]

    def update_active_tools(self, updated_prompt_and_tools: UpdatedPromptAndTools):
        if updated_prompt_and_tools.tools_to_activate:
            for tool in updated_prompt_and_tools.tools_to_activate:
                for (
                    validated_tool
                ) in self.retrieval_config.workflow_config.validated_tools:
                    if tool == validated_tool.name:
                        self.retrieval_config.workflow_config.activated_tools.append(
                            validated_tool
                        )

        if updated_prompt_and_tools.tools_to_deactivate:
            for tool in updated_prompt_and_tools.tools_to_deactivate:
                for (
                    activated_tool
                ) in self.retrieval_config.workflow_config.activated_tools:
                    if tool == activated_tool.name:
                        self.retrieval_config.workflow_config.activated_tools.remove(
                            activated_tool
                        )

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

        msg = custom_prompts.UPDATE_PROMPT.format(**inputs)

        response: UpdatedPromptAndTools

        try:
            structured_llm = self.llm_endpoint._llm.with_structured_output(
                UpdatedPromptAndTools, method="json_schema"
            )
            response = structured_llm.invoke(msg)

        except openai.BadRequestError:
            structured_llm = self.llm_endpoint._llm.with_structured_output(
                UpdatedPromptAndTools
            )
            response = structured_llm.invoke(msg)

        self.update_active_tools(response)
        self.retrieval_config.prompt = response.prompt

        # message = f"Updated system prompt: {response.content}"

        # formatted_response = {
        #     "answer": message,  # Assuming the last message contains the final answer
        # }
        # return {"messages": [message], "final_response": formatted_response}
        reasoning = [response.prompt_reasoning] if response.prompt_reasoning else []
        reasoning += [response.reasoning_tools] if response.reasoning_tools else []

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

    ### Nodes
    async def rewrite(self, state: AgentState) -> AgentState:
        """
        Transform the query to produce a better question.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with re-phrased question
        """

        tasks = state["tasks"]

        # Prepare the async tasks for all user tsks
        async_tasks = []
        for task in tasks:
            msg = custom_prompts.CONDENSE_QUESTION_PROMPT.format(
                chat_history=state["chat_history"].to_list(),
                question=task,
            )

            model = self.llm_endpoint._llm
            # Asynchronously invoke the model for each question
            async_tasks.append(model.ainvoke(msg))

        # Gather all the responses asynchronously
        responses = await asyncio.gather(*async_tasks) if async_tasks else []

        # Replace each question with its condensed version
        condensed_questions = []
        for response in responses:
            condensed_questions.append(response.content)

        return {**state, "tasks": condensed_questions}

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
            elif (
                chunk.metadata[config.relevance_score_key] >= relevance_score_threshold
            ):
                filtered_chunks.append(chunk)

        return filtered_chunks

    def websearch_split(self, state: AgentState):
        tasks = state["tasks"]
        if not tasks:
            return [Send("generate_rag", state)]

        docs = state["docs"]

        available_tools, activated_tools = collect_tools(
            self.retrieval_config.workflow_config
        )

        input = {
            "chat_history": state["chat_history"].to_list(),
            "tasks": state["tasks"],
            "context": docs,
            "available_tools": available_tools,
        }

        input, _ = self.reduce_rag_context(
            inputs=input,
            prompt=custom_prompts.WEBSEARCH_ROUTING_PROMPT,
            docs=docs,
            max_context_tokens=2000,
        )

        msg = custom_prompts.WEBSEARCH_ROUTING_PROMPT.format(**input)

        response: TasksCompletion

        try:
            structured_llm = self.llm_endpoint._llm.with_structured_output(
                TasksCompletion, method="json_schema"
            )
            response = structured_llm.invoke(msg)

        except openai.BadRequestError:
            structured_llm = self.llm_endpoint._llm.with_structured_output(
                TasksCompletion
            )
            response = structured_llm.invoke(msg)

        send_list: List[Send] = []

        if response.non_completable_tasks:
            payload = {
                **state,
                "tasks": response.non_completable_tasks,
            }
            send_list.append(Send("tavily_search", payload))
        else:
            send_list.append(Send("generate_rag", state))

        return send_list

    async def tavily_search(self, state: AgentState) -> AgentState:
        if not self.retrieval_config.workflow_config.activated_tools:
            return {**state}

        tasks = state["tasks"]

        tool_name = self.retrieval_config.workflow_config.activated_tools[0].name
        tool_wrapper = LLMToolFactory.create_tool(tool_name, {})

        # Prepare the async tasks for all questions
        async_tasks = []
        for task in tasks:
            formatted_input = tool_wrapper.format_input(task)
            # Asynchronously invoke the model for each question
            async_tasks.append(tool_wrapper.tool.ainvoke(formatted_input))

        # Gather all the responses asynchronously
        responses = await asyncio.gather(*async_tasks) if async_tasks else []

        docs = []
        for response in responses:
            _docs = tool_wrapper.format_output(response)
            _docs = self.filter_chunks_by_relevance(_docs)
            docs += _docs

        return {**state, "docs": state["docs"] + docs}

    async def retrieve(self, state: AgentState) -> AgentState:
        """
        Retrieve relevent chunks

        Args:
            state (messages): The current state

        Returns:
            dict: The retrieved chunks
        """

        tasks = state["tasks"]
        if not tasks:
            return {**state, "docs": []}

        kwargs = {
            "search_kwargs": {
                "k": self.retrieval_config.k,
            }
        }  # type: ignore
        base_retriever = self.get_retriever(**kwargs)

        kwargs = {"top_n": self.retrieval_config.reranker_config.top_n}  # type: ignore
        reranker = self.get_reranker(**kwargs)

        compression_retriever = ContextualCompressionRetriever(
            base_compressor=reranker, base_retriever=base_retriever
        )

        # Prepare the async tasks for all questions
        async_tasks = []
        for task in tasks:
            # Asynchronously invoke the model for each question
            async_tasks.append(compression_retriever.ainvoke(task))

        # Gather all the responses asynchronously
        responses = await asyncio.gather(*async_tasks) if async_tasks else []

        docs = []
        for response in responses:
            _docs = self.filter_chunks_by_relevance(response)
            docs += _docs

        return {**state, "docs": docs}

    async def dynamic_retrieve(self, state: AgentState) -> AgentState:
        """
        Retrieve relevent chunks

        Args:
            state (messages): The current state

        Returns:
            dict: The retrieved chunks
        """

        tasks = state["tasks"]
        if not tasks:
            return {**state, "docs": []}

        k = self.retrieval_config.k
        top_n = self.retrieval_config.reranker_config.top_n
        number_of_relevant_chunks = top_n
        i = 1

        while number_of_relevant_chunks == top_n:
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
            async_tasks = []
            for task in tasks:
                # Asynchronously invoke the model for each question
                async_tasks.append(compression_retriever.ainvoke(task))

            # Gather all the responses asynchronously
            responses = await asyncio.gather(*async_tasks) if async_tasks else []

            docs = []
            _n = []
            for response in responses:
                _docs = self.filter_chunks_by_relevance(response)
                _n.append(len(_docs))
                docs += _docs

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

        return {**state, "docs": docs}

    def get_rag_context_length(self, state: AgentState, docs: List[Document]) -> int:
        messages = state["messages"]
        user_question = messages[0].content
        files = state["files"]

        prompt = self.retrieval_config.prompt

        final_inputs = {}
        final_inputs["question"] = user_question
        final_inputs["custom_instructions"] = prompt if prompt else "None"
        final_inputs["files"] = files if files else "None"
        final_inputs["chat_history"] = state["chat_history"].to_list()

        final_inputs["context"] = combine_documents(docs) if docs else "None"
        msg = custom_prompts.RAG_ANSWER_PROMPT.format(**final_inputs)

        return self.llm_endpoint.count_tokens(msg)

    def reduce_rag_context(
        self,
        inputs: Dict[str, Any],
        prompt: BasePromptTemplate,
        docs: List[Document] | None = None,
        max_context_tokens: int | None = None,
    ) -> Tuple[Dict[str, Any], List[Document] | None]:
        MAX_ITERATION = 100
        SECURITY_FACTOR = 0.85
        iteration = 0

        msg = prompt.format(**inputs)
        n = self.llm_endpoint.count_tokens(msg)
        reduced_inputs = deepcopy(inputs)

        max_context_tokens = (
            max_context_tokens
            if max_context_tokens
            else self.retrieval_config.llm_config.max_context_tokens
        )

        while n > max_context_tokens * SECURITY_FACTOR:
            chat_history = (
                reduced_inputs["chat_history"]
                if "chat_history" in reduced_inputs
                else []
            )

            if len(chat_history) > 0:
                reduced_inputs["chat_history"] = chat_history[2:]
            elif docs and len(docs) > 1:
                docs = docs[:-1]
            else:
                logging.warning(
                    f"Not enough context to reduce. The context length is {n} "
                    f"which is greater than the max context tokens of {max_context_tokens}"
                )
                break

            if docs and "context" in reduced_inputs:
                reduced_inputs["context"] = combine_documents(docs)

            msg = prompt.format(**reduced_inputs)
            n = self.llm_endpoint.count_tokens(msg)

            iteration += 1
            if iteration > MAX_ITERATION:
                logging.warning(
                    f"Attained the maximum number of iterations ({MAX_ITERATION})"
                )
                break

        return reduced_inputs, docs

    def bind_tools_to_llm(self, node_name: str):
        if self.llm_endpoint.supports_func_calling():
            tools = self.retrieval_config.workflow_config.get_node_tools(node_name)
            llm_copy = self.llm_endpoint.clone_llm()  # Clone the LLM
            llm_copy = llm_copy.bind_tools(tools, tool_choice="any")
            return llm_copy
        return self.llm_endpoint._llm

    def generate_rag(self, state: AgentState) -> AgentState:
        messages = state["messages"]
        user_question = messages[0].content
        files = state["files"]

        docs: List[Document] | None = state["docs"]

        prompt = self.retrieval_config.prompt

        final_inputs = {}
        final_inputs["context"] = combine_documents(docs) if docs else "None"
        final_inputs["question"] = user_question
        final_inputs["custom_instructions"] = prompt if prompt else "None"
        final_inputs["files"] = files if files else "None"
        final_inputs["chat_history"] = state["chat_history"].to_list()
        final_inputs["reasoning"] = state["reasoning"]
        available_tools, activated_tools = collect_tools(
            self.retrieval_config.workflow_config
        )
        final_inputs["tools"] = available_tools

        reduced_inputs, docs = self.reduce_rag_context(
            final_inputs, prompt=custom_prompts.RAG_ANSWER_PROMPT, docs=docs
        )

        msg = custom_prompts.RAG_ANSWER_PROMPT.format(**reduced_inputs)

        llm = self.bind_tools_to_llm(self.generate_rag.__name__)
        response = llm.invoke(msg)
        return {**state, "messages": [response], "docs": docs if docs else []}

    def generate_chat_llm(self, state: AgentState) -> AgentState:
        """
        Generate answer

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with re-phrased question
        """
        messages = state["messages"]
        user_question = messages[0].content

        # Prompt
        prompt = self.retrieval_config.prompt

        final_inputs = {}
        final_inputs["question"] = user_question
        final_inputs["custom_instructions"] = prompt if prompt else "None"
        final_inputs["chat_history"] = state["chat_history"].to_list()

        # LLM
        llm = self.llm_endpoint._llm

        reduced_inputs, _ = self.reduce_rag_context(
            final_inputs, prompt=custom_prompts.CHAT_LLM_PROMPT
        )

        msg = custom_prompts.CHAT_LLM_PROMPT.format(**reduced_inputs)

        # Run
        response = llm.invoke(msg)
        return {**state, "messages": [response]}

    def build_chain(self):
        """
        Builds the langchain chain for the given configuration.

        Returns:
            Callable[[Dict], Dict]: The langchain chain.
        """
        if not self.graph:
            self.graph = self.create_graph()

        return self.graph

    def create_graph(self):
        """
        Builds the langchain chain for the given configuration.

        This function creates a state machine which takes a chat history and a question
        and produces an answer. The state machine consists of the following states:

        - filter_history: Filter the chat history (i.e., remove the last message)
        - rewrite: Re-write the question using the filtered history
        - retrieve: Retrieve documents related to the re-written question
        - generate: Generate an answer using the retrieved documents

        The state machine starts in the filter_history state and transitions as follows:
        filter_history -> rewrite -> retrieve -> generate -> END

        The final answer is returned as a dictionary with the answer and the list of documents
        used to generate the answer.

        Returns:
            Callable[[Dict], Dict]: The langchain chain.
        """
        workflow = StateGraph(AgentState)

        self.final_nodes: List[str] = []

        if self.retrieval_config.workflow_config:
            for node in self.retrieval_config.workflow_config.nodes:
                if node.name not in [START, END]:
                    workflow.add_node(node.name, getattr(self, node.name))

            for node in self.retrieval_config.workflow_config.nodes:
                if node.edges:
                    for edge in node.edges:
                        workflow.add_edge(node.name, edge)
                        if edge == END:
                            self.final_nodes.append(node.name)
                elif node.conditional_edge:
                    routing_function = getattr(
                        self, node.conditional_edge.routing_function
                    )
                    workflow.add_conditional_edges(
                        node.name, routing_function, node.conditional_edge.conditions
                    )
                    if isinstance(node.conditional_edge.conditions, dict):
                        values = node.conditional_edge.conditions.values()
                    else:
                        values = node.conditional_edge.conditions
                    if END in values:
                        self.final_nodes.append(node.name)
                else:
                    raise ValueError(
                        "Node should have at least one edge or conditional_edge"
                    )
        else:
            # Define the nodes we will cycle between
            workflow.add_node("filter_history", self.filter_history)
            workflow.add_node("rewrite", self.rewrite)  # Re-writing the question
            workflow.add_node("retrieve", self.retrieve)  # retrieval
            workflow.add_node("generate", self.generate_rag)

            # Add node for filtering history

            workflow.set_entry_point("filter_history")
            workflow.add_edge("filter_history", "rewrite")
            workflow.add_edge("rewrite", "retrieve")
            workflow.add_edge("retrieve", "generate")
            workflow.add_edge(
                "generate", END
            )  # Add edge from generate to format_response

        # Compile
        graph = workflow.compile()
        return graph

    async def answer_astream(
        self,
        question: str,
        history: ChatHistory,
        list_files: list[QuivrKnowledge],
        metadata: dict[str, str] = {},
    ) -> AsyncGenerator[ParsedRAGChunkResponse, ParsedRAGChunkResponse]:
        """
        Answer a question using the langgraph chain and yield each chunk of the answer separately.

        Args:
            question (str): The question to answer.
            history (ChatHistory): The chat history to use for context.
            list_files (list[QuivrKnowledge]): The list of files to use for retrieval.
            metadata (dict[str, str], optional): The metadata to pass to the langchain invocation. Defaults to {}.

        Yields:
            ParsedRAGChunkResponse: Each chunk of the answer.
        """
        concat_list_files = format_file_list(
            list_files, self.retrieval_config.max_files
        )
        conversational_qa_chain = self.build_chain()

        rolling_message = AIMessageChunk(content="")
        docs: list[Document] | None = None
        prev_answer = ""
        chunk_id = 0

        async for event in conversational_qa_chain.astream_events(
            {
                "messages": [
                    ("user", question),
                ],
                "chat_history": history,
                "files": concat_list_files,
            },
            version="v1",
            config={"metadata": metadata},
        ):
            if (
                not docs
                and "output" in event["data"]
                and event["data"]["output"] is not None
                and "docs" in event["data"]["output"]
                and event["metadata"]["langgraph_node"] in self.final_nodes
            ):
                docs = event["data"]["output"]["docs"]

            if (
                event["event"] == "on_chat_model_stream"
                and "langgraph_node" in event["metadata"]
                and event["metadata"]["langgraph_node"] in self.final_nodes
            ):
                chunk = event["data"]["chunk"]
                rolling_message, answer_str = parse_chunk_response(
                    rolling_message,
                    chunk,
                    self.llm_endpoint.supports_func_calling(),
                )
                if len(answer_str) > 0:
                    if (
                        self.llm_endpoint.supports_func_calling()
                        and rolling_message.tool_calls
                    ):
                        diff_answer = answer_str[len(prev_answer) :]
                        if len(diff_answer) > 0:
                            parsed_chunk = ParsedRAGChunkResponse(
                                answer=diff_answer,
                                metadata=get_chunk_metadata(rolling_message, docs),
                            )
                            prev_answer += diff_answer

                            logger.debug(
                                f"answer_astream func_calling=True question={question} rolling_msg={rolling_message} chunk_id={chunk_id}, chunk={parsed_chunk}"
                            )
                            yield parsed_chunk
                    else:
                        parsed_chunk = ParsedRAGChunkResponse(
                            answer=answer_str,
                            metadata=get_chunk_metadata(rolling_message, docs),
                        )
                        logger.debug(
                            f"answer_astream func_calling=False question={question} rolling_msg={rolling_message} chunk_id={chunk_id}, chunk={parsed_chunk}"
                        )
                        yield parsed_chunk

                    chunk_id += 1

        # Last chunk provides metadata
        last_chunk = ParsedRAGChunkResponse(
            answer="",  # Ensure no citations are appended to the answer
            metadata=get_chunk_metadata(rolling_message, docs),
            last_chunk=True,
        )
        logger.debug(
            f"answer_astream last_chunk={last_chunk} question={question} rolling_msg={rolling_message} chunk_id={chunk_id}"
        )
        yield last_chunk
