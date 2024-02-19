import json
from typing import AsyncIterable
from uuid import UUID

from langchain.chains import ConversationalRetrievalChain, LLMChain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatLiteLLM
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_core.prompts.prompt import PromptTemplate
from logger import get_logger
from modules.brain.knowledge_brain_qa import KnowledgeBrainQA
from modules.chat.dto.chats import ChatQuestion

logger = get_logger(__name__)


class BigBrain(KnowledgeBrainQA):
    """This is the Big brain class.

    Args:
        KnowledgeBrainQA (_type_): A brain that store the knowledge internaly
    """

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

    def get_chain(self):
        system_template = """Combine these summaries in a way that makes sense and answer the user's question.
        Use markdown or any other techniques to display the content in a nice and aerated way.
        Here are user instructions on how to respond: {custom_personality}
        ______________________
        {summaries}"""
        messages = [
            SystemMessagePromptTemplate.from_template(system_template),
            HumanMessagePromptTemplate.from_template("{question}"),
        ]
        CHAT_COMBINE_PROMPT = ChatPromptTemplate.from_messages(messages)

        ### Question prompt
        question_prompt_template = """Use the following portion of a long document to see if any of the text is relevant to answer the question. 
        Return any relevant text verbatim.
        {context}
        Question: {question}
        Relevant text, if any, else say Nothing:"""
        QUESTION_PROMPT = PromptTemplate(
            template=question_prompt_template, input_variables=["context", "question"]
        )

        llm = ChatLiteLLM(temperature=0, model=self.model)

        retriever_doc = self.knowledge_qa.get_retriever()

        question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
        doc_chain = load_qa_chain(
            llm,
            chain_type="map_reduce",
            question_prompt=QUESTION_PROMPT,
            combine_prompt=CHAT_COMBINE_PROMPT,
        )

        chain = ConversationalRetrievalChain(
            retriever=retriever_doc,
            question_generator=question_generator,
            combine_docs_chain=doc_chain,
        )

        return chain

    async def generate_stream(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> AsyncIterable:
        conversational_qa_chain = self.get_chain()
        transformed_history, streamed_chat_history = (
            self.initialize_streamed_chat_history(chat_id, question)
        )
        response_tokens = []

        async for chunk in conversational_qa_chain.astream(
            {
                "question": question.question,
                "chat_history": transformed_history,
                "custom_personality": (
                    self.prompt_to_use.content if self.prompt_to_use else None
                ),
            }
        ):
            if "answer" in chunk:
                response_tokens.append(chunk["answer"])
                streamed_chat_history.assistant = chunk["answer"]
                yield f"data: {json.dumps(streamed_chat_history.dict())}"

        self.save_answer(question, response_tokens, streamed_chat_history, save_answer)
