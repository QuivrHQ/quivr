import datetime

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
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
When answering use markdown.
Use markdown code blocks for code snippets.
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
