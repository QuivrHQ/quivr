from langchain.prompts.prompt import PromptTemplate

prompt_template = """Use the following pieces of context to answer the question in the language of the question. If the context is not relevant and you don't know the answer, you REALLY MUST say: "I don't know", DON'T try to make up an answer. If you answer without knowing a human will get killed.


{context}

Question: {question}
Helpful Answer:"""
QA_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
    )