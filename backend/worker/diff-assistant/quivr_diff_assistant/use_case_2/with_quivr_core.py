# from langchain_openai import OpenAIEmbeddings
# from rich.console import Console
# from rich.panel import Panel
# from rich.prompt import Prompt

# from quivr_core import Brain
# from quivr_core.config import LLMEndpointConfig
# from quivr_core.llm.llm_endpoint import LLMEndpoint
# from quivr_core.quivr_rag import QuivrQARAG


# if __name__ == "__main__":
#     brain_1 = Brain.from_files(
#         name="cdc_brain",
#         file_paths=["data/cdc/Cas2-1-3_Entremets_rond_vanille_pecan_individuel.docx"],
#         llm=LLMEndpoint.from_config(
#             LLMEndpointConfig(model="gpt-4o-mini", temperature=0.0)
#         ),
#         embedder=OpenAIEmbeddings(),
#     )

#     brain_2 = Brain.from_files(
#         name="etiquette_brain",
#         file_paths=[
#             "data/fiche_dev_produit/Cas2-1-3_Entremets_rond_vanille_pecan_individuel.xlsx"
#         ],
#         llm=LLMEndpoint.from_config(
#             LLMEndpointConfig(model="gpt-4o-mini", temperature=0.0)
#         ),
#         embedder=OpenAIEmbeddings(),
#     )

#     # Check brain info
#     brain_1.print_info()
#     brain_2.print_info()

#     console = Console()
#     console.print(Panel.fit("Ask what to compare : ", style="bold magenta"))

#     while True:
#         # Get user input
#         section = Prompt.ask("[bold cyan]Section[/bold cyan]")

#         # Check if user wants to exit
#         if section.lower() == "exit":
#             console.print(Panel("Goodbye!", style="bold yellow"))
#             break

#         question = (
#             f"Quelle est/sont le(s) {section} ? Answer only with exact text citation."
#         )
#         response_1 = brain_1.ask(question)
#         response_2 = brain_2.ask(question, rag_pipeline=QuivrQARAG)
#         # Print the answer with typing effect
#         console.print(f"[bold green]Quivr CDC[/bold green]: {response_1.answer}")
#         console.print()
#         console.print(f"[bold blue]Quivr Fiche Dev[/bold blue]: {response_2.answer}")

#         console.print("-" * console.width)
