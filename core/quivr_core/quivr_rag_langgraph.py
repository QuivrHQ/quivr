import logging
from enum import Enum
from typing import Annotated, AsyncGenerator, Optional, Sequence, TypedDict
from uuid import uuid4

# TODO(@aminediro): this is the only dependency to langchain package, we should remove it
from langchain.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from langchain_community.document_compressors import JinaRerank
from langchain_core.callbacks import Callbacks
from langchain_core.documents import BaseDocumentCompressor, Document
from langchain_core.messages import BaseMessage
from langchain_core.messages.ai import AIMessageChunk
from langchain_core.vectorstores import VectorStore
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from quivr_core.chat import ChatHistory
from quivr_core.config import DefaultRerankers, RetrievalConfig
from quivr_core.llm import LLMEndpoint
from quivr_core.models import (
    ParsedRAGChunkResponse,
    ParsedRAGResponse,
    QuivrKnowledge,
    RAGResponseMetadata,
    cited_answer,
)
from quivr_core.prompts import custom_prompts
from quivr_core.utils import (
    combine_documents,
    format_file_list,
    get_chunk_metadata,
    parse_chunk_response,
    parse_response,
)

logger = logging.getLogger("quivr_core")


class SpecialEdges(str, Enum):
    START = "START"
    END = "END"


class AgentState(TypedDict):
    # The add_messages function defines how an update should be processed
    # Default is to replace. add_messages says "append"
    messages: Annotated[Sequence[BaseMessage], add_messages]
    chat_history: ChatHistory
    docs: list[Document]
    files: str
    final_response: dict


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
        reranker: BaseDocumentCompressor | None = None,
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

        if reranker is not None:
            self.reranker = reranker
        elif self.retrieval_config.reranker_config.supplier == DefaultRerankers.COHERE:
            self.reranker = CohereRerank(
                model=self.retrieval_config.reranker_config.model,
                top_n=self.retrieval_config.reranker_config.top_n,
                cohere_api_key=self.retrieval_config.reranker_config.api_key,
            )
        elif self.retrieval_config.reranker_config.supplier == DefaultRerankers.JINA:
            self.reranker = JinaRerank(
                model=self.retrieval_config.reranker_config.model,
                top_n=self.retrieval_config.reranker_config.top_n,
                jina_api_key=self.retrieval_config.reranker_config.api_key,
            )
        else:
            self.reranker = IdempotentCompressor()

        if self.vector_store:
            self.compression_retriever = ContextualCompressionRetriever(
                base_compressor=self.reranker, base_retriever=self.retriever
            )

    @property
    def retriever(self):
        """
        Returns a retriever that can retrieve documents from the vector store.

        Returns:
            VectorStoreRetriever: The retriever.
        """
        if self.vector_store:
            return self.vector_store.as_retriever()
        else:
            raise ValueError("No vector store provided")

    def filter_history(self, state: AgentState) -> dict:
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
                > self.retrieval_config.llm_config.max_output_tokens
                or total_pairs >= self.retrieval_config.max_history
            ):
                break
            _chat_history.append(human_message)
            _chat_history.append(ai_message)
            total_tokens += message_tokens
            total_pairs += 1

        return {"chat_history": _chat_history}

    ### Nodes
    def rewrite(self, state):
        """
        Transform the query to produce a better question.

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with re-phrased question
        """

        # Grader
        msg = custom_prompts.CONDENSE_QUESTION_PROMPT.format(
            chat_history=state["chat_history"],
            question=state["messages"][0].content,
        )

        model = self.llm_endpoint._llm
        response = model.invoke(msg)
        return {"messages": [response]}

    def retrieve(self, state):
        """
        Retrieve relevent chunks

        Args:
            state (messages): The current state

        Returns:
            dict: The retrieved chunks
        """
        question = state["messages"][-1].content
        docs = self.compression_retriever.invoke(question)
        return {"docs": docs}

    def generate_rag(self, state):
        """
        Generate answer

        Args:
            state (messages): The current state

        Returns:
            dict: The updated state with re-phrased question
        """
        messages = state["messages"]
        user_question = messages[0].content
        files = state["files"]

        docs = state["docs"]

        # Prompt
        prompt = self.retrieval_config.prompt

        final_inputs = {}
        final_inputs["context"] = combine_documents(docs) if docs else "None"
        final_inputs["question"] = user_question
        final_inputs["custom_instructions"] = prompt if prompt else "None"
        final_inputs["files"] = files if files else "None"

        # LLM
        llm = self.llm_endpoint._llm
        if self.llm_endpoint.supports_func_calling():
            llm = self.llm_endpoint._llm.bind_tools(
                [cited_answer],
                tool_choice="any",
            )

        # Chain
        rag_chain = custom_prompts.RAG_ANSWER_PROMPT | llm

        # Run
        response = rag_chain.invoke(final_inputs)
        formatted_response = {
            "answer": response,  # Assuming the last message contains the final answer
            "docs": docs,
        }
        return {"messages": [response], "final_response": formatted_response}

    def generate_chat_llm(self, state):
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

        # Chain
        rag_chain = custom_prompts.CHAT_LLM_PROMPT | llm

        # Run
        response = rag_chain.invoke(final_inputs)
        formatted_response = {
            "answer": response,  # Assuming the last message contains the final answer
        }
        return {"messages": [response], "final_response": formatted_response}

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

        if self.retrieval_config.workflow_config:
            if SpecialEdges.START not in [
                node.name for node in self.retrieval_config.workflow_config.nodes
            ]:
                raise ValueError("The workflow should contain a 'START' node")
            for node in self.retrieval_config.workflow_config.nodes:
                if node.name not in SpecialEdges._value2member_map_:
                    workflow.add_node(node.name, getattr(self, node.name))

            for node in self.retrieval_config.workflow_config.nodes:
                for edge in node.edges:
                    if node.name == SpecialEdges.START:
                        workflow.add_edge(START, edge)
                    elif edge == SpecialEdges.END:
                        workflow.add_edge(node.name, END)
                    else:
                        workflow.add_edge(node.name, edge)
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

    def answer(
        self,
        question: str,
        history: ChatHistory,
        list_files: list[QuivrKnowledge],
        metadata: dict[str, str] = {},
    ) -> ParsedRAGResponse:
        """
        Answer a question using the langgraph chain.

        Args:
            question (str): The question to answer.
            history (ChatHistory): The chat history to use for context.
            list_files (list[QuivrKnowledge]): The list of files to use for retrieval.
            metadata (dict[str, str], optional): The metadata to pass to the langchain invocation. Defaults to {}.

        Returns:
            ParsedRAGResponse: The answer to the question.
        """
        concat_list_files = format_file_list(
            list_files, self.retrieval_config.max_files
        )
        conversational_qa_chain = self.build_chain()
        inputs = {
            "messages": [
                ("user", question),
            ],
            "chat_history": history,
            "files": concat_list_files,
        }
        raw_llm_response = conversational_qa_chain.invoke(
            inputs,
            config={"metadata": metadata},
        )
        response = parse_response(
            raw_llm_response["final_response"], self.retrieval_config.llm_config.model
        )
        return response

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
        sources: list[Document] | None = None
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
            kind = event["event"]
            if (
                not sources
                and "output" in event["data"]
                and "docs" in event["data"]["output"]
            ):
                sources = event["data"]["output"]["docs"]

            if (
                kind == "on_chat_model_stream"
                and "generate" in event["metadata"]["langgraph_node"]
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
                                metadata=RAGResponseMetadata(),
                            )
                            prev_answer += diff_answer

                            logger.debug(
                                f"answer_astream func_calling=True question={question} rolling_msg={rolling_message} chunk_id={chunk_id}, chunk={parsed_chunk}"
                            )
                            yield parsed_chunk
                    else:
                        parsed_chunk = ParsedRAGChunkResponse(
                            answer=answer_str,
                            metadata=RAGResponseMetadata(),
                        )
                        logger.debug(
                            f"answer_astream func_calling=False question={question} rolling_msg={rolling_message} chunk_id={chunk_id}, chunk={parsed_chunk}"
                        )
                        yield parsed_chunk

                    chunk_id += 1

        # Last chunk provides metadata
        last_chunk = ParsedRAGChunkResponse(
            answer="",
            metadata=get_chunk_metadata(rolling_message, sources),
            last_chunk=True,
        )
        logger.debug(
            f"answer_astream last_chunk={last_chunk} question={question} rolling_msg={rolling_message} chunk_id={chunk_id}"
        )
        yield last_chunk
