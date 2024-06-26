import json
from typing import AsyncIterable, List
from uuid import UUID

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)
from langchain_core.pydantic_v1 import BaseModel as BaseModelV1
from langchain_core.pydantic_v1 import Field as FieldV1
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from quivr_api.logger import get_logger
from quivr_api.modules.brain.knowledge_brain_qa import KnowledgeBrainQA
from quivr_api.modules.chat.dto.chats import ChatQuestion
from quivr_api.modules.chat.dto.outputs import GetChatHistoryOutput
from quivr_api.modules.chat.service.chat_service import ChatService
from quivr_api.modules.dependencies import get_service
from typing_extensions import TypedDict


# Post-processing
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
    """

    question: str
    generation: str
    documents: List[str]


# Data model
class GradeDocuments(BaseModelV1):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = FieldV1(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )


class GradeHallucinations(BaseModelV1):
    """Binary score for hallucination present in generation answer."""

    binary_score: str = FieldV1(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )


# Data model
class GradeAnswer(BaseModelV1):
    """Binary score to assess answer addresses question."""

    binary_score: str = FieldV1(
        description="Answer addresses the question, 'yes' or 'no'"
    )


logger = get_logger(__name__)

chat_service = get_service(ChatService)()


class SelfBrain(KnowledgeBrainQA):
    """
    GPT4Brain integrates with GPT-4 to provide real-time answers and supports various tools to enhance its capabilities.

    Available Tools:
    - WebSearchTool: Performs web searches to find relevant information.
    - ImageGeneratorTool: Generates images based on textual descriptions.
    - URLReaderTool: Reads and summarizes content from URLs.
    - EmailSenderTool: Sends emails with specified content.

    Use Cases:
    - WebSearchTool can be used to find the latest news articles on a specific topic or to gather information from various websites.
    - ImageGeneratorTool is useful for creating visual content based on textual prompts, such as generating a company logo based on a description.
    - URLReaderTool can be used to summarize articles or web pages, making it easier to quickly understand the content without reading the entire text.
    - EmailSenderTool enables automated email sending, such as sending a summary of a meeting's minutes to all participants.
    """

    max_input: int = 10000

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

    def calculate_pricing(self):
        return 3

    def retrieval_grade(self):
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        structured_llm_grader = llm.with_structured_output(GradeDocuments)

        # Prompt
        system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
            It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
            If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
            Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""
        grade_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                (
                    "human",
                    "Retrieved document: \n\n {document} \n\n User question: {question}",
                ),
            ]
        )

        retrieval_grader = grade_prompt | structured_llm_grader

        return retrieval_grader

    def generation_rag(self):
        # Prompt
        human_prompt = """You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

        Question: {question} 

        Context: {context} 

        Answer:
        """
        prompt_human = PromptTemplate.from_template(human_prompt)
        # LLM
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

        # Chain
        rag_chain = prompt_human | llm | StrOutputParser()

        return rag_chain

    def hallucination_grader(self):
        # LLM with function call
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        structured_llm_grader = llm.with_structured_output(GradeHallucinations)

        # Prompt
        system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
            Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts."""
        hallucination_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                (
                    "human",
                    "Set of facts: \n\n {documents} \n\n LLM generation: {generation}",
                ),
            ]
        )

        hallucination_grader = hallucination_prompt | structured_llm_grader

        return hallucination_grader

    def answer_grader(self):
        # LLM with function call
        llm = ChatOpenAI(model="gpt-4o", temperature=0)
        structured_llm_grader = llm.with_structured_output(GradeAnswer)

        # Prompt
        system = """You are a grader assessing whether an answer addresses / resolves a question \n 
            Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""
        answer_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                (
                    "human",
                    "User question: \n\n {question} \n\n LLM generation: {generation}",
                ),
            ]
        )

        answer_grader = answer_prompt | structured_llm_grader

        return answer_grader

    def question_rewriter(self):
        # LLM
        llm = ChatOpenAI(model="gpt-4o", temperature=0)

        # Prompt
        system = """You a question re-writer that converts an input question to a better version that is optimized \n 
            for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning."""
        re_write_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system),
                (
                    "human",
                    "Here is the initial question: \n\n {question} \n Formulate an improved question.",
                ),
            ]
        )

        question_rewriter = re_write_prompt | llm | StrOutputParser()

        return question_rewriter

    def get_chain(self):

        graph = self.create_graph()

        return graph

    def create_graph(self):

        workflow = StateGraph(GraphState)

        # Define the nodes
        workflow.add_node("retrieve", self.retrieve)  # retrieve
        workflow.add_node("grade_documents", self.grade_documents)  # grade documents
        workflow.add_node("generate", self.generate)  # generatae
        workflow.add_node("transform_query", self.transform_query)  # transform_query

        # Build graph
        workflow.set_entry_point("retrieve")
        workflow.add_edge("retrieve", "grade_documents")
        workflow.add_conditional_edges(
            "grade_documents",
            self.decide_to_generate,
            {
                "transform_query": "transform_query",
                "generate": "generate",
            },
        )
        workflow.add_edge("transform_query", "retrieve")
        workflow.add_conditional_edges(
            "generate",
            self.grade_generation_v_documents_and_question,
            {
                "not supported": "generate",
                "useful": END,
                "not useful": "transform_query",
            },
        )

        # Compile
        app = workflow.compile()
        return app

    def retrieve(self, state):
        """
        Retrieve documents

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, documents, that contains retrieved documents
        """
        print("---RETRIEVE---")
        logger.info("Retrieving documents")
        question = state["question"]
        logger.info(f"Question: {question}")

        # Retrieval
        retriever = self.knowledge_qa.get_retriever()
        documents = retriever.get_relevant_documents(question)
        return {"documents": documents, "question": question}

    def generate(self, state):
        """
        Generate answer

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, generation, that contains LLM generation
        """
        print("---GENERATE---")
        question = state["question"]
        documents = state["documents"]

        formatted_docs = format_docs(documents)
        # RAG generation
        generation = self.generation_rag().invoke(
            {"context": formatted_docs, "question": question}
        )
        return {"documents": documents, "question": question, "generation": generation}

    def grade_documents(self, state):
        """
        Determines whether the retrieved documents are relevant to the question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates documents key with only filtered relevant documents
        """

        print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
        question = state["question"]
        documents = state["documents"]

        # Score each doc
        filtered_docs = []
        for d in documents:
            score = self.retrieval_grade().invoke(
                {"question": question, "document": d.page_content}
            )
            grade = score.binary_score
            if grade == "yes":
                print("---GRADE: DOCUMENT RELEVANT---")
                filtered_docs.append(d)
            else:
                print("---GRADE: DOCUMENT NOT RELEVANT---")
                continue
        return {"documents": filtered_docs, "question": question}

    def transform_query(self, state):
        """
        Transform the query to produce a better question.

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): Updates question key with a re-phrased question
        """

        print("---TRANSFORM QUERY---")
        question = state["question"]
        documents = state["documents"]

        # Re-write question
        better_question = self.question_rewriter().invoke({"question": question})
        return {"documents": documents, "question": better_question}

    def decide_to_generate(self, state):
        """
        Determines whether to generate an answer, or re-generate a question.

        Args:
            state (dict): The current graph state

        Returns:
            str: Binary decision for next node to call
        """

        print("---ASSESS GRADED DOCUMENTS---")
        question = state["question"]
        filtered_documents = state["documents"]

        if not filtered_documents:
            # All documents have been filtered check_relevance
            # We will re-generate a new query
            print(
                "---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---"
            )
            return "transform_query"
        else:
            # We have relevant documents, so generate answer
            print("---DECISION: GENERATE---")
            return "generate"

    def grade_generation_v_documents_and_question(self, state):
        """
        Determines whether the generation is grounded in the document and answers question.

        Args:
            state (dict): The current graph state

        Returns:
            str: Decision for next node to call
        """

        print("---CHECK HALLUCINATIONS---")
        question = state["question"]
        documents = state["documents"]
        generation = state["generation"]

        score = self.hallucination_grader().invoke(
            {"documents": documents, "generation": generation}
        )
        grade = score.binary_score

        # Check hallucination
        if grade == "yes":
            print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
            # Check question-answering
            print("---GRADE GENERATION vs QUESTION---")
            score = self.answer_grader().invoke(
                {"question": question, "generation": generation}
            )
            grade = score.binary_score
            if grade == "yes":
                print("---DECISION: GENERATION ADDRESSES QUESTION---")
                return "useful"
            else:
                print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
                return "not useful"
        else:
            print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
            return "not supported"

    async def generate_stream(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> AsyncIterable:
        conversational_qa_chain = self.get_chain()
        transformed_history, streamed_chat_history = (
            self.initialize_streamed_chat_history(chat_id, question)
        )
        filtered_history = self.filter_history(transformed_history, 40, 2000)
        response_tokens = []
        config = {"metadata": {"conversation_id": str(chat_id)}}

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are GPT-4 powered by Quivr. You are an assistant. {custom_personality}",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )
        prompt_formated = prompt.format_messages(
            chat_history=filtered_history,
            question=question.question,
            custom_personality=(
                self.prompt_to_use.content if self.prompt_to_use else None
            ),
        )

        async for event in conversational_qa_chain.astream(
            {"question": question.question}, config=config
        ):
            for key, value in event.items():
                if "generation" in value and value["generation"] != "":
                    response_tokens.append(value["generation"])
                    streamed_chat_history.assistant = value["generation"]

                    yield f"data: {json.dumps(streamed_chat_history.dict())}"

        self.save_answer(question, response_tokens, streamed_chat_history, save_answer)

    def generate_answer(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> GetChatHistoryOutput:
        conversational_qa_chain = self.get_chain()
        transformed_history, _ = self.initialize_streamed_chat_history(
            chat_id, question
        )
        filtered_history = self.filter_history(transformed_history, 40, 2000)
        config = {"metadata": {"conversation_id": str(chat_id)}}

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are GPT-4 powered by Quivr. You are an assistant. {custom_personality}",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )
        prompt_formated = prompt.format_messages(
            chat_history=filtered_history,
            question=question.question,
            custom_personality=(
                self.prompt_to_use.content if self.prompt_to_use else None
            ),
        )
        model_response = conversational_qa_chain.invoke(
            {"messages": prompt_formated},
            config=config,
        )

        answer = model_response["messages"][-1].content

        return self.save_non_streaming_answer(
            chat_id=chat_id, question=question, answer=answer, metadata={}
        )
