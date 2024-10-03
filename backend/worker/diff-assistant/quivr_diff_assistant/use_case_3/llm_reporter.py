from typing import List

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts.prompt import PromptTemplate

from quivr_diff_assistant.use_case_3.diff_type import DiffResult

REPORT_PROMPT = PromptTemplate.from_template(
    template="""You are tasked with analyzing and reporting differences in text for a Quality engineer. The input text contains differences marked with special tokens. Your job is to parse these differences and create a clear, concise report.

                        Here is the text containing the differences:

                        <diff_text>
                        {text_modified}
                        </diff_text>

                        RULE #1 : If there are no [[->]] tokens, it indicates no changes to report, inventing changes means death.
                        The differences are marked using the following format:
                        - [[before->after]] indicates a change from "before" to "after"
                        - If there is no "before" text, it indicates an addition
                        - If there is no "after" text, it indicates a deletion
                        - If there is no [[    ]] token, it indicates no changes to report
                        - Make sense of the difference and do not keep the '[' in the report.
                        - "_" alone means empty.

                        Follow these steps to create your report:

                        1. Carefully read through the entire text.
                        2. Identify each instance of [[ ]] tokens.
                        3. For each instance, determine the modification that was made.
                        Present your report in the following markdown format:
                        
                        # Title (Difference Report)
                        ## Section Name
                        ### Subsection Name (if applicable)
                        * Original: Original text
                        * Modified: Modified text
                        * Changes:
                            * Change 1
                            * Change 2
                            * Change 3

                        Avoid repetitive infos, only report the changes.
                        Keep the checkbox when possible and compare the correct check box.
                        
                        
                        Every modification should be clearly stated with the original text and the modified text.
                        Note that there might be no modifications in some sections. In that case, simply return nothing.
                        Try to make the report as clear and concise as possible, a point for each modification found with details, avoid big comparisons.


                        Remember, your goal is to create a clear and concise report that allows the Quality engineer to quickly verify the differences. Focus on accuracy and readability in your output, give every indication possible to make it easier to find the modification.
                        The report should be written in a professional and formal tone and in French.""",
)


def redact_report(difference_per_section: List[DiffResult], llm: BaseChatModel) -> str:
    report_per_section = []
    combined_diffs = ""
    for section in difference_per_section:
        if len(section.diffs) == 1 and section.diffs[0][0] == 0:
            print("No differences found in this section.")
            continue
        combined_diffs += str(section)

    chain = REPORT_PROMPT | llm
    result = chain.invoke({"text_modified": str(combined_diffs)})
    report_per_section.append(result.content)

    report_text = ""

    for rep in report_per_section:
        report_text += "\n".join(rep.split("\n")[1:-1]) + "\n\n"
    return report_text
