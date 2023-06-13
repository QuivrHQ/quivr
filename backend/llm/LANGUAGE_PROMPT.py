from langchain.prompts.prompt import PromptTemplate

prompt_template = """ONLY Use the following pieces of context to answer the question in the language of the question. If the context is not relevant and you don't know the answer, you REALLY MUST say: "I don't know, i'm only your second brain 🧠", DON'T try to make up an answer. If you answer without knowing from the given context a human will get killed. DONT assume.


{context}

Question: {question}
Helpful Answer:"""
QA_PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
    )