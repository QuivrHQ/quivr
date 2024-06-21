from typing import List

import pandas as pd
from bs4 import BeautifulSoup
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

GENERIC_PROMPT = """You will be generating questions to verify the compliance of items based on a provided document. Here is the document:
<document>
{DOCUMENT}
</document>

<document_context>
{DOCUMENT_CONTEXT}
</document_context>

Please follow these steps to generate the questions:

Carefully review the document and items table to understand the context and requirements. Review the input language to know in which language you should generate the questions.
Extract the individual raw items from the items table. For composed items, break them down into their sub-items. Focus on the raw items only, not the composed items themselves.
For each raw item, formulate a specific question to verify its compliance with the requirements outlined in the document. The question should be in the format: "Is [item information] compliant with the requirements?"
When generating each question, include all relevant information about the item so that the question can be answered without needing to refer back to the items table. This is important because the team verifying the items will not have access to the table.
Before providing the final questions, write out your thought process and reasoning inside <scratchpad> tags. Explain how you extracted the raw items and formulated each question.
Finally, avoiding repetitive questions, output the generated questions inside <questions> tags, with each question on a separate line.

Remember, the goal is to create specific, informative questions for each raw item to verify compliance with the requirements outlined in the document. Make sure to provide all necessary context within the questions themselves. Write the most question possible.
"""
# answer in the language of the question only

DOCUMENT_CONTEXT = """
The document is a list of specificity for a pastry product, every ingredient listed must be verified to be accepted by the Coup de Pates company.
Extract the individual raw ingredients from the ingredients table. For composed ingredients, break them down into their sub-ingredients. Focus on the raw ingredients only, not the composed ingredients themselves.
When generating each question, include all relevant information about the ingredient so that the question can be answered without needing to refer back to the ingredients table. This is important because the team verifying the ingredients will not have access to the table.
Look for the most detail in each ingredient, such as the labels (RSPCO, élevés en cage), do not add the country it is from, do not add the name of the parent ingredient (ex: BASE VERTE)
Note that a recipe that is not precised to be gluten free is by default not gluten free, also try to note which king of product it is (a pastry ? a salted dish ?)
Do not ask for an ingredient that is not raw, only raw ingredients are to be verified such as sugar, additifs, oil, colorants, etc.

The questions must be specific to a unique ingredient at each time.
The number of questions should match the number of unique ingredients in the document.
The question will be asked directly to the "Charte Qualité" team, they won't have access to the provided document.

Exemple : 
Document states : The product is composed of a green base containing sugar, flour, and eggs from outdors raised chicken.
questions : ["Is Sugar compliant with the requirements?", "Is Flour compliant with the requirements?", "Is Eggs from outdors raised chicken compliant with the requirements?]
"""


class QuestionType(BaseModel):
    """Represent a list of questions translated in a specific language."""

    language: str = Field(description="Language of the generated questions.")
    questions: List[str] = Field(
        description="List of generated questions in the right language."
    )


class QuestionGenerator:
    def __init__(self, document_context=None):
        self.generic_prompt = GENERIC_PROMPT
        self.document_context = (
            document_context if document_context else DOCUMENT_CONTEXT
        )

    def table_to_text(self, df):
        text_rows = []
        for _, row in df.iterrows():
            row_text = " | ".join(str(value) for value in row.values if pd.notna(value))
            if row_text:
                text_rows.append("|" + row_text + "|")
        return "\n".join(text_rows)

    def generate_questions(
        self, target_content: str, language_verification: bool = False
    ) -> list[str]:
        target_text = target_content

        print("Generating Questions ...")

        prompt = PromptTemplate(
            template=self.generic_prompt,
            input_variables=["DOCUMENT", "DOCUMENT_CONTEXT"],
        )

        llm = ChatOpenAI(model="gpt-4o", temperature=0.0)
        llm_chain = prompt | llm

        questions = llm_chain.invoke(
            {"DOCUMENT": target_text, "DOCUMENT_CONTEXT": self.document_context}
        )

        soup = BeautifulSoup(str(questions.content), "html.parser")
        questions_content = soup.find("questions").text  # type: ignore

        if language_verification:
            print("Verifying language and translating questions ...")
            model = ChatOpenAI(model="gpt-4o", temperature=0.0)

            # Set up a parser + inject instructions into the prompt template.
            parser = PydanticOutputParser(pydantic_object=QuestionType)

            prompt = PromptTemplate(
                template="Translate the following questions in french.\n{format_instructions}\n{questions}\n",
                input_variables=["questions"],
                partial_variables={
                    "format_instructions": parser.get_format_instructions()
                },
            )

            # And a query intended to prompt a language model to populate the data structure.
            prompt_and_model = prompt | model
            questions = prompt_and_model.invoke({"questions": questions_content})
            translated_question: QuestionType = parser.invoke(questions)

            return translated_question.questions

        return str(questions_content).split("\n")
