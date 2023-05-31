from langchain.prompts.prompt import PromptTemplate

_template = """Given the following conversation and a follow up question. User's question might be in different language each time, response needs to be in the same language as user's current question everytime. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

prompt_template = """Use the following pieces of context to answer. User's question might be in different language each time, response needs to be in the same language as user's current question everytime. If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}

Question: {question}
Helpful Answer:"""
QA_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
    )