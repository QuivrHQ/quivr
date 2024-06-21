import asyncio

import pandas as pd
from pydantic import BaseModel, Field

from .query_engine import DecisionEnum, DiffQueryEngine
from .question_generator import QuestionGenerator


class ResponseType(BaseModel):
    """Represents an ingredient and its associated decision."""

    name: str | None = Field(description="Name of the ingredient")
    detailed_answer: str | None = Field(description="Detailed answer with explanations")
    decision: DecisionEnum | None = Field(
        description="Decision made: authorized / to avoid / forbidden"
    )


class ContextType(BaseModel):
    """Represents the context given and the specific category if needed."""

    category: str = Field(description="Category of the context")
    context: str = Field(description="Context to add to the query")


"""

"""


class DifferenceAgent:
    def __init__(
        self,
        diff_query_engine: DiffQueryEngine,
        document_context: str | None = None,
        question_generator: QuestionGenerator | None = None,
    ):
        self.document_context = document_context
        self.question_generator = (
            question_generator
            if question_generator
            else QuestionGenerator(document_context=document_context)
        )
        self.diff_query_engine = diff_query_engine

        self.questions = None
        self.generated_df = pd.DataFrame()

    def generate_questions(
        self, target_content: str, language_verification: bool = False
    ) -> list[str] | None:

        self.questions = self.question_generator.generate_questions(
            target_content=target_content, language_verification=language_verification
        )

    def run(
        self,
        target_content: str | None = None,
        language_verification: bool = False,
        additional_context: ContextType | None = None,
        verbose: bool = False,
        n_retry: int = 3,
    ):
        if self.questions is None and target_content:
            self.questions = self.generate_questions(
                target_content=target_content,
                language_verification=language_verification,
            )
        elif self.questions is None:
            raise Exception(
                f"Please provide a source path and tab name to generate questions"
            )

        print("Querying generated questions to the reference document...")
        analysis = []

        async def query_all(questions):
            return await asyncio.gather(*[query_one(question) for question in questions])  # type: ignore

        async def query_one(question):
            response = ResponseType(name=None, detailed_answer=None, decision=None)

            for i in range(n_retry):
                try:
                    response: ResponseType = await self.diff_query_engine.query_engine.aquery(question[:-1])  # type: ignore
                    nodes_to_update = [response.source_nodes[int(i)] for i in response.response.used_chunks]  # type: ignore
                    self.diff_query_engine.update_query_engine(nodes_to_update)

                except Exception as e:
                    print(e)
                    if verbose:
                        print(f"Error with question: {question}")
                        print("Retry ...")
                        if i == 2:
                            print(
                                f"{n_retry} repeted errors with the same question, deleting the question."
                            )
                            break
                        continue
                break
            return {
                "decision": (
                    response.decision.value if response.decision else response.decision
                ),
                "name": response.name,
                "detailed_answer": response.detailed_answer,
            }

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        try:
            analysis = loop.run_until_complete(query_all(self.questions))
            self.generated_df = pd.DataFrame(analysis)
            return self.generated_df
        finally:
            if loop.is_running():
                loop.close()

    def get_detail(self, category, iteration, name):
        return self.generated_df.loc[
            self.generated_df["name"] == name,
            [f"{category}.{iteration}.detail", f"{category}.{iteration}"],
        ]

    """
    Later : DVC (git) / clearML 
    """
