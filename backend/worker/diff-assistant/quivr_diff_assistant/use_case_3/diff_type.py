from typing import List, Tuple

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts.prompt import PromptTemplate

DIFF_PROMPT = PromptTemplate.from_template(
    template="""
    You need to compare two texts and report all the differences. Your job is to parse these differences and create a clear, concise report. \
        Organize the report by sections and provide a detailed explanation of each difference. \
            Be specific on difference, it will be reviewed and verified by a Quality engineer.
    Here are the different sections of the report:
    * Dénominations, comprenant:
        * dénomination légale: nom du produit tel qu’il est défini par la réglementation, \
            en général cela inclut aussi avec des information sur son état (cuite, cru, gelé ... )
        * dénomination commercial: nom du produit tel qu’il est vendu au consommateur
    * Ingrédients et allergènes en français, comprenant:
        * liste d’ingrédients
        * traces d’allergènes
        * Une sous-section pour chaque sous produit si il y a lieu;
    * Ingrédients et allergènes en anglais, comprenant:
        * liste d’ingrédients
        * traces d’allergènes
        * Une sous-section pour chaque sous produit si il y a lieu;
    * Eléments de traçabilité, comprenant:
        * le code-barre EAN
        * le code article
        * DDM - date de durabilité minimale
        * numéro de lot
        * date de fabrication
        * adresse de l'entreprise
    * Conseils d’utilisation / de manipulation produit, comprenant :
        * Conditions de remise en oeuvre
        * Durée de vie
        * Conditions de transport
        * Conditions de conservation : « A conserver à -18°C / Ne pas recongeler un produit décongeler »
        * Temps de decongelation
        * Temperature de prechauffage
    * Poids du produit
    * Valeurs / informations nutritionnelles
    * Autres

    Notes:
     -> Coup de Pates: Tradition & Innovation, est l'entreprise productrice / marque du produit.

    Chaque sections doivent être organisées comme suit et séparées par des lignes entre chaque avant et après:

    ## section_name

    **Avant** : ...

    **Après** : ...

    **Modifications**:
        * ...
        * ...


    -----TEXT BEFORE MODIFICATION-----
    {before_text}
    -----TEXT AFTER MODIFICATION-----
    {after_text}

    The report should be written in a professional and formal tone and in French.
    """
)


class DiffResult:
    def __init__(self, diffs: List[Tuple[int, str]]) -> None:
        self.diffs = diffs

    def remove_dummy_diffs(self) -> None:
        cleaned_diff = []
        for cat, content in self.diffs:
            if content.strip() and content != "\n":
                cleaned_diff.append((cat, content))

        self.diffs = cleaned_diff

    def format_diffs(self) -> str:
        text_modified = ""

        sub_stack = 0
        for op, data in self.diffs:
            if op == 0:
                text_modified += data if sub_stack == 0 else f"_]] {data}"
            elif op == -1:
                if sub_stack == 0:
                    text_modified += f"[[{data}->"
                    sub_stack += 1
                else:
                    text_modified += f"{data}->"
            elif op == 1:
                if sub_stack > 0:
                    text_modified += f"{data}]]"
                    sub_stack -= 1
                else:
                    text_modified += f"[[ _ ->{data}]]"

        return text_modified

    def __str__(self) -> str:
        return self.format_diffs()


def llm_comparator(before_text: str, after_text: str, llm: BaseChatModel) -> str:
    chain = DIFF_PROMPT | llm
    result = chain.invoke({"before_text": before_text, "after_text": after_text})
    return str(result.content)
