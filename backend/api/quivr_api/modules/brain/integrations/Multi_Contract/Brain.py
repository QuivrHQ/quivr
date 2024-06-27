import datetime
from operator import itemgetter
from typing import List

from langchain.prompts import HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_community.chat_models import ChatLiteLLM
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.pydantic_v1 import BaseModel as BaseModelV1
from langchain_core.pydantic_v1 import Field as FieldV1
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI
from quivr_api.logger import get_logger
from quivr_api.modules.brain.knowledge_brain_qa import KnowledgeBrainQA

logger = get_logger(__name__)


class cited_answer(BaseModelV1):
    """Answer the user question based only on the given sources, and cite the sources used."""

    thoughts: str = FieldV1(
        ...,
        description="""Description of the thought process, based only on the given sources. 
        Cite the text as much as possible and give the document name it appears in. In the format : 'Doc_name states : cited_text'. Be the most 
        procedural as possible.""",
    )
    answer: str = FieldV1(
        ...,
        description="The answer to the user question, which is based only on the given sources.",
    )
    citations: List[int] = FieldV1(
        ...,
        description="The integer IDs of the SPECIFIC sources which justify the answer.",
    )

    thoughts: str = FieldV1(
        ...,
        description="Explain shortly what you did to find the answer and what you used by citing the sources by their name.",
    )
    followup_questions: List[str] = FieldV1(
        ...,
        description="Generate up to 3 follow-up questions that could be asked based on the answer given or context provided.",
    )


# First step is to create the Rephrasing Prompt
_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language. Keep as much details as possible from previous messages. Keep entity names and all.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

# Next is the answering prompt

template_answer = """
Context:
{context}

User Question: {question}
Answer:
"""

today_date = datetime.datetime.now().strftime("%B %d, %Y")

system_message_template = (
    f"Your name is Quivr. You're a helpful assistant. Today's date is {today_date}."
)

system_message_template += """
When answering use markdown neat.
Answer in a concise and clear manner.
Use the following pieces of context from files provided by the user to answer the users.
Answer in the same language as the user question.
If you don't know the answer with the context provided from the files, just say that you don't know, don't try to make up an answer.
Don't cite the source id in the answer objects, but you can use the source to answer the question.
You have access to the files to answer the user question (limited to first 20 files):
{files}

If not None, User instruction to follow to answer: {custom_instructions}
Don't cite the source id in the answer objects, but you can use the source to answer the question.
"""


ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(system_message_template),
        HumanMessagePromptTemplate.from_template(template_answer),
    ]
)


# How we format documents

DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(
    template="Source: {index} \n {page_content}"
)


class MultiContractBrain(KnowledgeBrainQA):
    """
    The MultiContract class integrates advanced conversational retrieval and language model chains
    to provide comprehensive and context-aware responses to user queries.

    It leverages a combination of document retrieval, question condensation, and document-based
    question answering to generate responses that are informed by a wide range of knowledge sources.
    """

    def __init__(
        self,
        **kwargs,
    ):
        """
        Initializes the MultiContract class with specific configurations.

        Args:
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(
            **kwargs,
        )

    def get_chain(self):

        list_files_array = (
            self.knowledge_qa.knowledge_service.get_all_knowledge_in_brain(
                self.brain_id
            )
        )  # pyright: ignore reportPrivateUsage=none

        list_files_array = [file.file_name for file in list_files_array]
        # Max first 10 files
        if len(list_files_array) > 20:
            list_files_array = list_files_array[:20]

        list_files = "\n".join(list_files_array) if list_files_array else "None"

        retriever_doc = self.knowledge_qa.get_retriever()

        loaded_memory = RunnablePassthrough.assign(
            chat_history=RunnableLambda(
                lambda x: self.filter_history(x["chat_history"]),
            ),
            question=lambda x: x["question"],
        )

        api_base = None
        if self.brain_settings.ollama_api_base_url and self.model.startswith("ollama"):
            api_base = self.brain_settings.ollama_api_base_url

        standalone_question = {
            "standalone_question": {
                "question": lambda x: x["question"],
                "chat_history": itemgetter("chat_history"),
            }
            | CONDENSE_QUESTION_PROMPT
            | ChatLiteLLM(temperature=0, model=self.model, api_base=api_base)
            | StrOutputParser(),
        }

        knowledge_qa = self.knowledge_qa
        prompt_custom_user = knowledge_qa.prompt_to_use()
        prompt_to_use = "None"
        if prompt_custom_user:
            prompt_to_use = prompt_custom_user.content

        # Now we retrieve the documents
        retrieved_documents = {
            "docs": itemgetter("standalone_question") | retriever_doc,
            "question": lambda x: x["standalone_question"],
            "custom_instructions": lambda x: prompt_to_use,
        }

        final_inputs = {
            "context": lambda x: self.knowledge_qa._combine_documents(x["docs"]),
            "question": itemgetter("question"),
            "custom_instructions": itemgetter("custom_instructions"),
            "files": lambda x: list_files,
        }
        llm = ChatLiteLLM(
            max_tokens=self.max_tokens,
            model=self.model,
            temperature=self.temperature,
            api_base=api_base,
        )  # pyright: ignore reportPrivateUsage=none
        if self.model_compatible_with_function_calling(self.model):

            # And finally, we do the part that returns the answers
            llm_function = ChatOpenAI(
                max_tokens=self.max_tokens,
                model=self.model,
                temperature=self.temperature,
            )
            llm = llm_function.bind_tools(
                [cited_answer],
                tool_choice="cited_answer",
            )

        answer = {
            "answer": final_inputs | ANSWER_PROMPT | llm,
            "docs": itemgetter("docs"),
        }

        return loaded_memory | standalone_question | retrieved_documents | answer
