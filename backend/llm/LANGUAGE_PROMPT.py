from langchain.prompts.prompt import PromptTemplate

prompt_template = """Use the following pieces of context to answer the question in the language of the question. If you don't know the answer, just say that you don't know, don't try to make up an answer.


{context}

Question: {question}
Helpful Answer:"""
QA_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
    )