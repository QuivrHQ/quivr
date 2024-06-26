import json
import operator
from typing import Annotated, AsyncIterable, List, Optional, Sequence, TypedDict
from uuid import UUID

from langchain.tools import BaseTool
from langchain_core.messages import BaseMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from quivr_api.logger import get_logger
from quivr_api.modules.brain.knowledge_brain_qa import KnowledgeBrainQA
from quivr_api.modules.chat.dto.chats import ChatQuestion
from quivr_api.modules.chat.dto.outputs import GetChatHistoryOutput
from quivr_api.modules.chat.service.chat_service import ChatService
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.tools import (
    EmailSenderTool,
    ImageGeneratorTool,
    URLReaderTool,
    WebSearchTool,
)


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]


logger = get_logger(__name__)

chat_service = get_service(ChatService)()


class GPT4Brain(KnowledgeBrainQA):
    """
    GPT4Brain integrates with GPT-4 to provide real-time answers and supports various tools to enhance its capabilities.

    Available Tools:
    - WebSearchTool: Performs web searches to find relevant information.
    - ImageGeneratorTool: Generates images based on textual descriptions.
    - URLReaderTool: Reads and summarizes content from URLs.
    - EmailSenderTool: Sends emails with specified content.

    Use Cases:
    - WebSearchTool can be used to find the latest news articles on a specific topic or to gather information from various websites.
    - ImageGeneratorTool is useful for creating visual content based on textual prompts, such as generating a company logo based on a description.
    - URLReaderTool can be used to summarize articles or web pages, making it easier to quickly understand the content without reading the entire text.
    - EmailSenderTool enables automated email sending, such as sending a summary of a meeting's minutes to all participants.
    """

    tools: Optional[List[BaseTool]] = None
    tool_executor: Optional[ToolExecutor] = None
    function_model: ChatOpenAI = None

    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )
        self.tools = [
            WebSearchTool(),
            ImageGeneratorTool(),
            URLReaderTool(),
            EmailSenderTool(user_email=self.user_email),
        ]
        self.tool_executor = ToolExecutor(tools=self.tools)

    def calculate_pricing(self):
        return 3

    def should_continue(self, state):
        messages = state["messages"]
        last_message = messages[-1]
        # Make sure there is a previous message

        if last_message.tool_calls:
            name = last_message.tool_calls[0]["name"]
            if name == "image-generator":
                return "final"
        # If there is no function call, then we finish
        if not last_message.tool_calls:
            return "end"
        # Otherwise if there is, we check if it's suppose to return direct
        else:
            return "continue"

    # Define the function that calls the model
    def call_model(self, state):
        messages = state["messages"]
        response = self.function_model.invoke(messages)
        # We return a list, because this will get added to the existing list
        return {"messages": [response]}

    # Define the function to execute tools
    def call_tool(self, state):
        messages = state["messages"]
        # Based on the continue condition
        # we know the last message involves a function call
        last_message = messages[-1]
        # We construct an ToolInvocation from the function_call
        tool_call = last_message.tool_calls[0]
        tool_name = tool_call["name"]
        arguments = tool_call["args"]

        action = ToolInvocation(
            tool=tool_call["name"],
            tool_input=tool_call["args"],
        )
        # We call the tool_executor and get back a response
        response = self.tool_executor.invoke(action)
        # We use the response to create a FunctionMessage
        function_message = ToolMessage(
            content=str(response), name=action.tool, tool_call_id=tool_call["id"]
        )
        # We return a list, because this will get added to the existing list
        return {"messages": [function_message]}

    def create_graph(self):
        # Define a new graph
        workflow = StateGraph(AgentState)

        # Define the two nodes we will cycle between
        workflow.add_node("agent", self.call_model)
        workflow.add_node("action", self.call_tool)
        workflow.add_node("final", self.call_tool)

        # Set the entrypoint as `agent`
        # This means that this node is the first one called
        workflow.set_entry_point("agent")

        # We now add a conditional edge
        workflow.add_conditional_edges(
            # First, we define the start node. We use `agent`.
            # This means these are the edges taken after the `agent` node is called.
            "agent",
            # Next, we pass in the function that will determine which node is called next.
            self.should_continue,
            # Finally we pass in a mapping.
            # The keys are strings, and the values are other nodes.
            # END is a special node marking that the graph should finish.
            # What will happen is we will call `should_continue`, and then the output of that
            # will be matched against the keys in this mapping.
            # Based on which one it matches, that node will then be called.
            {
                # If `tools`, then we call the tool node.
                "continue": "action",
                # Final call
                "final": "final",
                # Otherwise we finish.
                "end": END,
            },
        )

        # We now add a normal edge from `tools` to `agent`.
        # This means that after `tools` is called, `agent` node is called next.
        workflow.add_edge("action", "agent")
        workflow.add_edge("final", END)

        # Finally, we compile it!
        # This compiles it into a LangChain Runnable,
        # meaning you can use it as you would any other runnable
        app = workflow.compile()
        return app

    def get_chain(self):
        self.function_model = ChatOpenAI(model="gpt-4o", temperature=0, streaming=True)

        self.function_model = self.function_model.bind_tools(self.tools)

        graph = self.create_graph()

        return graph

    async def generate_stream(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> AsyncIterable:
        conversational_qa_chain = self.get_chain()
        transformed_history, streamed_chat_history = (
            self.initialize_streamed_chat_history(chat_id, question)
        )
        filtered_history = self.filter_history(transformed_history, 40, 2000)
        response_tokens = []
        config = {"metadata": {"conversation_id": str(chat_id)}}

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are GPT-4 powered by Quivr. You are an assistant. {custom_personality}",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )
        prompt_formated = prompt.format_messages(
            chat_history=filtered_history,
            question=question.question,
            custom_personality=(
                self.prompt_to_use.content if self.prompt_to_use else None
            ),
        )

        async for event in conversational_qa_chain.astream_events(
            {"messages": prompt_formated},
            config=config,
            version="v1",
        ):
            kind = event["event"]
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    # Empty content in the context of OpenAI or Anthropic usually means
                    # that the model is asking for a tool to be invoked.
                    # So we only print non-empty content
                    response_tokens.append(content)
                    streamed_chat_history.assistant = content
                    yield f"data: {json.dumps(streamed_chat_history.dict())}"
            elif kind == "on_tool_start":
                print("--")
                print(
                    f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
                )
            elif kind == "on_tool_end":
                print(f"Done tool: {event['name']}")
                print(f"Tool output was: {event['data'].get('output')}")
                print("--")
            elif kind == "on_chain_end":
                output = event["data"]["output"]
                final_output = [item for item in output if "final" in item]
                if final_output:
                    if (
                        final_output[0]["final"]["messages"][0].name
                        == "image-generator"
                    ):
                        final_message = final_output[0]["final"]["messages"][0].content
                        response_tokens.append(final_message)
                        streamed_chat_history.assistant = final_message
                        yield f"data: {json.dumps(streamed_chat_history.dict())}"

        self.save_answer(question, response_tokens, streamed_chat_history, save_answer)

    def generate_answer(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> GetChatHistoryOutput:
        conversational_qa_chain = self.get_chain()
        transformed_history, _ = self.initialize_streamed_chat_history(
            chat_id, question
        )
        filtered_history = self.filter_history(transformed_history, 40, 2000)
        config = {"metadata": {"conversation_id": str(chat_id)}}

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are GPT-4 powered by Quivr. You are an assistant. {custom_personality}",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{question}"),
            ]
        )
        prompt_formated = prompt.format_messages(
            chat_history=filtered_history,
            question=question.question,
            custom_personality=(
                self.prompt_to_use.content if self.prompt_to_use else None
            ),
        )
        model_response = conversational_qa_chain.invoke(
            {"messages": prompt_formated},
            config=config,
        )

        answer = model_response["messages"][-1].content

        return self.save_non_streaming_answer(
            chat_id=chat_id, question=question, answer=answer, metadata={}
        )
