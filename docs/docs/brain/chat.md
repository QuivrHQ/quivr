## ChatHistory

The `ChatHistory` class is where all the conversation between the user and the LLM gets stored. A `ChatHistory` object will transparently be instanciated in the `Brain` every time you create one.

At each interaction with `Brain.ask_streaming` both your message and the LLM's response are added to this chat history. It's super handy because this history is used in the Retrieval-Augmented Generation (RAG) process to give the LLM more context, working as form of memory between the user and the system and helping it generate better responses by looking at what’s already been said.

You can also get some cool info about the brain by printing its details with the `print_info()` method, which shows things like how many chats are stored, the current chat history, and more. This makes it easy to keep track of what’s going on in your conversations and manage the context being sent to the LLM!

::: quivr_core.rag.entities.chat
options:
heading_level: 2
