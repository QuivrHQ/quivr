from dataclasses import dataclass
from uuid import UUID

from rich.tree import Tree


@dataclass
class ChatHistoryInfo:
    nb_chats: int
    current_default_chat: UUID
    current_chat_history_length: int

    def add_to_tree(self, chats_tree: Tree):
        chats_tree.add(f"Number of Chats: [bold]{self.nb_chats}[/bold]")
        chats_tree.add(
            f"Current Default Chat: [bold magenta]{self.current_default_chat}[/bold magenta]"
        )
        chats_tree.add(
            f"Current Chat History Length: [bold]{self.current_chat_history_length}[/bold]"
        )


@dataclass
class LLMInfo:
    model: str
    llm_base_url: str
    temperature: float
    max_tokens: int
    supports_function_calling: int

    def add_to_tree(self, llm_tree: Tree):
        llm_tree.add(f"Model: [italic]{self.model}[/italic]")
        llm_tree.add(f"Base URL: [underline]{self.llm_base_url}[/underline]")
        llm_tree.add(f"Temperature: [bold]{self.temperature}[/bold]")
        llm_tree.add(f"Max Tokens: [bold]{self.max_tokens}[/bold]")

        func_call_color = "green" if self.supports_function_calling else "red"
        llm_tree.add(
            f"Supports Function Calling: [bold {func_call_color}]{self.supports_function_calling}[/bold {func_call_color}]"
        )


@dataclass
class StorageInfo:
    storage_type: str
    n_files: int

    def add_to_tree(self, files_tree: Tree):
        files_tree.add(f"Storage Type: [italic]{self.storage_type}[/italic]")
        files_tree.add(f"Number of Files: [bold]{self.n_files}[/bold]")


@dataclass
class BrainInfo:
    brain_id: UUID
    brain_name: str
    files_info: StorageInfo
    chats_info: ChatHistoryInfo
    llm_info: LLMInfo

    def to_tree(self):
        tree = Tree("📊 Brain Information")
        tree.add(f"🆔 ID: [bold cyan]{self.brain_id}[/bold cyan]")
        tree.add(f"🧠 Brain Name: [bold green]{self.brain_name}[/bold green]")

        files_tree = tree.add("📁 Files")
        self.files_info.add_to_tree(files_tree)

        chats_tree = tree.add("💬 Chats")
        self.chats_info.add_to_tree(chats_tree)

        llm_tree = tree.add("🤖 LLM")
        self.llm_info.add_to_tree(llm_tree)
        return tree
