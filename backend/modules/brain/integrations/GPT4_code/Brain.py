import json
import operator
from typing import Annotated, AsyncIterable, List, Sequence, TypedDict
from uuid import UUID

from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from logger import get_logger
from modules.brain.knowledge_brain_qa import KnowledgeBrainQA
from modules.chat.dto.chats import ChatQuestion
from modules.chat.dto.outputs import GetChatHistoryOutput
from modules.chat.service.chat_service import ChatService
from langchain.pydantic_v1 import Field 
from pydantic import BaseModel


class CodeGenerationOutput(BaseModel):
    """Code formatted Output"""

    prefix: str = Field(...,description="Description of the problem and approach")
    imports: str = Field(...,description="Code block import statements")
    code: str = Field(...,description="Code block not including import statements")
    #description: str = "Schema for code solutions to questions about the doc"

class AgentState(TypedDict):
    generation: CodeGenerationOutput
    messages_seq: Annotated[Sequence[BaseMessage], operator.add]
    messages: List[str]
    iterations: int
    error: str



# Define the function that determines whether to continue or not

logger = get_logger(__name__)

chat_service = ChatService()

class GPT4CodeBrain(KnowledgeBrainQA):
    """This is the Notion brain class. it is a KnowledgeBrainQA has the data is stored locally.
    It is going to call the Data Store internally to get the data.

    Args:
        KnowledgeBrainQA (_type_): A brain that store the knowledge internaly
    """

    #tools: List[BaseTool] = [DuckDuckGoSearchResults(), ImageGeneratorTool()]
    #tool_executor: ToolExecutor = ToolExecutor(tools)
    model_function: ChatOpenAI = None
    max_iterations: int = 3 
    prompt: ChatPromptTemplate = None
    count: int = 0 #FIXME: Delete
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            **kwargs,
        )

    def calculate_pricing(self):
        return 3

    def should_continue(self, state: AgentState):
        # messages = state["messages_seq"]
        # last_message = messages[-1] #type: ignore
        # # Make sure there is a previous message

        error: str = state["error"]
        iterations: int = state["iterations"]
        
        if error == "no":
            return "end"
        
        elif iterations < self.max_iterations:
            return "end"
        else:
            # else we try re generating an answer
            return "generate"

    # Define the function that calls the model
    def call_model(self, state: AgentState):
        messages = state["messages"]
        response = self.model_function.invoke(messages)
        # We return a list, because this will get added to the existing list
        return {"messages": [response]}
    
    def generate(self, state: AgentState):
        # State
        messages = state["messages"]
        iterations = state["iterations"]
        error = state["error"]

         # Check if we are called because of an error
        if error == "yes":
            messages += [
                (
                    "user",
                    "Now, try again. Invoke the code tool to structure the output with a prefix, imports, and code block:",
                )
            ]
        
        code_gen_chain = self.prompt | self.model_function.with_structured_output(CodeGenerationOutput)

        # Solution
        if error != "no":
            code_solution = code_gen_chain.invoke(
                {"chat_history": [""], "messages": messages}
            )
        messages += [
            (
                "assistant",
                f"{code_solution['prefix']} \n Imports: {code_solution['imports']} \n Code: {code_solution['code']}",
            )
        ]

        # Increment
        iterations = iterations + 1
        return {"generation": code_solution, "messages": messages, "iterations": iterations}
    

    def code_check(self, state: AgentState) -> AgentState:
        """
        Check code validity

        Args:
            state (dict): The current graph state

        Returns:
            state (dict): New key added to state, error
        """

        # State
        messages = state["messages"]
        code_solution = state["generation"]
        iterations = state["iterations"]
        messages_seq = state["messages_seq"]

        # Get solution components
        #prefix = code_solution.prefix
        imports = code_solution["imports"]
        code = code_solution["code"]

        # Check imports
        try:
            exec(imports)
        except Exception as e:
            error_message = [("user", f"Your solution failed the import test: {e}")]
            messages += error_message
            return {
                "generation": code_solution,
                "messages": messages,
                "iterations": iterations,
                "error": "yes",
                "messages_seq": messages_seq,
            }

        # Check execution
        try:
            exec(imports + "\n" + code)
        except Exception as e:
            error_message = [("user", f"Your solution failed the code execution test: {e}")]
            messages += error_message
            return {
                "generation": code_solution,
                "messages": messages,
                "iterations": iterations,
                "error": "yes",
                "messages_seq": messages_seq,
            }

        # No errors
        return {
            "generation": code_solution,
            "messages": messages,
            "iterations": iterations,
            "error": "no",
            "messages_seq": messages_seq,
        }

    def create_graph(self):
        # Define a new graph
        workflow = StateGraph(AgentState)

        # Define the two nodes we will cycle between
        workflow.add_node("generate", self.generate)  # generate solution
        workflow.add_node("code_check", self.code_check)  # check code
        #workflow.add_node("final", self.code_check)  # render the final message

        # Set the entrypoint as `agent`
        # This means that this node is the first one called
        workflow.set_entry_point("generate")
        workflow.add_edge("generate", "code_check")


        # We now add a conditional edge
        workflow.add_conditional_edges(
            # First, we define the start node. We use `agent`.
            # This means these are the edges taken after the `agent` node is called.
            "code_check",
            # Next, we pass in the function that will determine which node is called next.
            self.should_continue,
            # Finally we pass in a mapping.
            # The keys are strings, and the values are other nodes.
            # END is a special node marking that the graph should finish.
            # What will happen is we will call `should_continue`, and then the output of that
            # will be matched against the keys in this mapping.
            # Based on which one it matches, that node will then be called.
            {
                "end": END,
                "generate": "generate",
                #"final": "final"
            },
        )
        #workflow.add_edge("final", END)


        # We now add a normal edge from `tools` to `agent`.
        # This means that after `tools` is called, `agent` node is called next.
        #workflow.add_edge("reflect", "generate")

        # Finally, we compile it!
        # This compiles it into a LangChain Runnable,
        # meaning you can use it as you would any other runnable
        app = workflow.compile()
        return app

    def get_chain(self):
        self.model_function = ChatOpenAI(
            model="gpt-4-turbo", temperature=0, streaming=True
        )

        # self.model_function = self.model_function.bind_tools(self.tools)

        graph = self.create_graph()

        return graph

    async def generate_stream(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> AsyncIterable:
        conversational_qa_chain = self.get_chain()
        transformed_history, streamed_chat_history = (
            self.initialize_streamed_chat_history(chat_id, question)
        )
        filtered_history = self.filter_history(transformed_history, 20, 2000)
        response_tokens = []
        config = {"metadata": {"conversation_id": str(chat_id)}}

        self.prompt = ChatPromptTemplate.from_messages( #type: ignore
            [
                (
                    "system",
                    """You are a coding assistant. \n 
            Here is a full set of a specific documentation:  \n ------- \n  || \n ------- \n Answer the user 
            question based on the above provided documentation. Ensure any code you provide can be executed \n 
            with all required imports and variables defined. Structure your answer with a description of the code solution. \n
            Then list the imports. And finally list the functioning code block. Here is the user question:""",
                ),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{messages}"),
            ]
        )
        # prompt_formated = prompt.format_messages(
        #     chat_history=filtered_history,
        #     question=question.question,
        #     custom_personality=(
        #         self.prompt_to_use.content if self.prompt_to_use else None
        #     ),
        # )

        async for event in conversational_qa_chain.astream_events(
            {"messages": [("user", question)], "iterations": 0},
            config=config,
            version="v1",
        ):
            kind = event["event"]
            print("kind: ", kind)
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    # Empty content in the context of OpenAI or Anthropic usually means
                    # that the model is asking for a tool to be invoked.
                    # So we only print non-empty content
                    response_tokens.append(content)
                    streamed_chat_history.assistant = content
                    yield f"data: {json.dumps(streamed_chat_history.dict())}"
            elif kind == "on_chain_end":
                output = event["data"]["output"]
                print(f"OUTPUT #{self.count}: {output}")
                for item in output:
                    print("ITEM: ", item)
                print("LEN OUTPUT :", len(output))
                final_output = [item for item in output if "final" in item]
                print("Final : ", final_output)
                if final_output:
                    if (
                        final_output[0]["final"]["messages"][0].name
                        == "code-generator"
                    ):
                        final_message = final_output[0]["final"]["messages"][0].content
                        response_tokens.append(final_message)
                        streamed_chat_history.assistant = final_message
                        yield f"data: {json.dumps(streamed_chat_history.dict())}"
        self.count+=1

        self.save_answer(question, response_tokens, streamed_chat_history, save_answer)

    def generate_answer(
        self, chat_id: UUID, question: ChatQuestion, save_answer: bool = True
    ) -> GetChatHistoryOutput:
        conversational_qa_chain = self.get_chain()
        transformed_history, _ = self.initialize_streamed_chat_history(
            chat_id, question
        )
        filtered_history = self.filter_history(transformed_history, 20, 2000)

        config = {"metadata": {"conversation_id": str(chat_id)}}

        self.prompt = ChatPromptTemplate.from_messages( #type: ignore
            [
                (
                    "system",
                    """You are a coding assistant with expertise in LCEL, LangChain expression language. \n 
            Here is a full set of a specific documentation:  \n ------- \n ||  \n ------- \n Answer the user 
            question based on the above provided documentation. Ensure any code you provide can be executed \n 
            with all required imports and variables defined. Structure your answer with a description of the code solution. \n
            Then list the imports. And finally list the functioning code block. Here is the user question:""",
                ),
                #MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{messages}"),
            ]
        )
        # prompt_formated = prompt.format_messages(
        #     chat_history=filtered_history,
        #     question=question.question,
        #     custom_personality=(
        #         self.prompt_to_use.content if self.prompt_to_use else None
        #     ),
        # )
        model_response = conversational_qa_chain.invoke(
            {"messages": [("user", question)], "iterations": 0},
            config=config,
        )

        answer = model_response["messages"][-1].content

        return self.save_non_streaming_answer(
            chat_id=chat_id, question=question, answer=answer, metadata={}
        )
