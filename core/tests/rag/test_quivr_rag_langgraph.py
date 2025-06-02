import pytest
from unittest.mock import Mock, patch, AsyncMock
from uuid import uuid4

from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import END, START

from quivr_core.rag.entities.chat import ChatHistory
from quivr_core.rag.entities.config import (
    RetrievalConfig,
    LLMEndpointConfig,
    RerankerConfig,
    DefaultRerankers,
    WorkflowConfig,
    NodeConfig,
)
from quivr_core.rag.quivr_rag_langgraph import (
    QuivrQARAGLangGraph,
    SplittedInput,
    TasksCompletion,
    FinalAnswer,
    UpdatedPromptAndTools,
    UserTaskEntity,
    UserTasks,
    AgentState,
    IdempotentCompressor,
)


class TestUserTaskEntity:
    """Test the UserTaskEntity class."""

    def test_creation(self):
        """Test creating UserTaskEntity."""
        task_id = uuid4()
        task = UserTaskEntity(
            id=task_id, definition="Test task", docs=[], completable=False, tool=None
        )

        assert task.id == task_id
        assert task.definition == "Test task"
        assert task.docs == []
        assert not task.completable
        assert task.tool is None

    def test_has_tool(self):
        """Test has_tool method."""
        task = UserTaskEntity(id=uuid4(), definition="Test")

        assert not task.has_tool()

        task.tool = "search_tool"
        assert task.has_tool()

    def test_is_completable(self):
        """Test is_completable method."""
        task = UserTaskEntity(id=uuid4(), definition="Test")

        assert not task.is_completable()

        task.completable = True
        assert task.is_completable()


class TestUserTasks:
    """Test the UserTasks class."""

    def test_creation_empty(self):
        """Test creating empty UserTasks."""
        tasks = UserTasks()

        assert not tasks.has_tasks()
        assert tasks.ids == []
        assert tasks.definitions == []
        assert tasks.docs == []

    def test_creation_with_definitions(self):
        """Test creating UserTasks with task definitions."""
        task_definitions = ["Task 1", "Task 2"]
        tasks = UserTasks(task_definitions)

        assert tasks.has_tasks()
        assert len(tasks.ids) == 2
        assert tasks.definitions == task_definitions

    def test_iteration(self):
        """Test iterating over UserTasks."""
        tasks = UserTasks(["Task 1", "Task 2"])

        task_list = list(tasks)
        assert len(task_list) == 2
        assert all(isinstance(task, UserTaskEntity) for task in task_list)

    def test_set_docs(self):
        """Test setting docs for a task."""
        tasks = UserTasks(["Task 1"])
        task_id = tasks.ids[0]
        docs = [
            Document(
                page_content="test",
                metadata={"original_file_name": "test.pdf", "index": 0},
            )
        ]

        tasks.set_docs(task_id, docs)
        assert tasks(task_id).docs == docs

    def test_set_docs_invalid_id(self):
        """Test setting docs with invalid task ID."""
        tasks = UserTasks(["Task 1"])
        invalid_id = uuid4()

        with pytest.raises(ValueError, match="Task with id .* not found"):
            tasks.set_docs(invalid_id, [])

    def test_set_definition(self):
        """Test setting definition for a task."""
        tasks = UserTasks(["Task 1"])
        task_id = tasks.ids[0]

        tasks.set_definition(task_id, "Updated task")
        assert tasks(task_id).definition == "Updated task"

    def test_set_completion(self):
        """Test setting completion status for a task."""
        tasks = UserTasks(["Task 1"])
        task_id = tasks.ids[0]

        tasks.set_completion(task_id, True)
        assert tasks(task_id).completable is True

    def test_set_tool(self):
        """Test setting tool for a task."""
        tasks = UserTasks(["Task 1"])
        task_id = tasks.ids[0]

        tasks.set_tool(task_id, "search_tool")
        assert tasks(task_id).tool == "search_tool"

    def test_completable_and_non_completable_tasks(self):
        """Test filtering completable and non-completable tasks."""
        tasks = UserTasks(["Task 1", "Task 2"])

        # Mark first task as completable
        tasks.set_completion(tasks.ids[0], True)

        completable = tasks.completable_tasks
        non_completable = tasks.non_completable_tasks

        assert len(completable) == 1
        assert len(non_completable) == 1
        assert tasks.has_non_completable_tasks()


class TestIdempotentCompressor:
    """Test the IdempotentCompressor class."""

    def test_compress_documents(self):
        """Test that compress_documents returns documents unchanged."""
        compressor = IdempotentCompressor()
        docs = [
            Document(
                page_content="doc1",
                metadata={"original_file_name": "test1.pdf", "index": 0},
            ),
            Document(
                page_content="doc2",
                metadata={"original_file_name": "test2.pdf", "index": 1},
            ),
        ]

        result = compressor.compress_documents(docs, "test query")

        assert result == docs


class TestQuivrQARAGLangGraph:
    """Test the QuivrQARAGLangGraph class."""

    @pytest.fixture
    def simple_retrieval_config(self):
        """Create a simple retrieval config that won't trigger validation errors."""
        with patch.dict("os.environ", {}, clear=True):
            return RetrievalConfig(
                llm_config=LLMEndpointConfig(
                    model="gpt-4o", max_context_tokens=128000, max_output_tokens=4096
                ),
                reranker_config=RerankerConfig(),
                workflow_config=WorkflowConfig(
                    nodes=[
                        NodeConfig(name=START, edges=["generate_rag"]),
                        NodeConfig(name="generate_rag", edges=[END]),
                    ]
                ),
            )

    @pytest.fixture
    def rag_instance(self, simple_retrieval_config, fake_llm, mem_vector_store):
        """Create a QuivrQARAGLangGraph instance."""
        return QuivrQARAGLangGraph(
            retrieval_config=simple_retrieval_config,
            llm=fake_llm,
            vector_store=mem_vector_store,
        )

    def test_initialization(
        self, rag_instance, simple_retrieval_config, fake_llm, mem_vector_store
    ):
        """Test QuivrQARAGLangGraph initialization."""
        assert rag_instance.retrieval_config == simple_retrieval_config
        assert rag_instance.llm_endpoint == fake_llm
        assert rag_instance.vector_store == mem_vector_store
        assert rag_instance.graph is None

    def test_get_reranker_cohere(self, rag_instance):
        """Test getting Cohere reranker."""
        with patch("quivr_core.rag.quivr_rag_langgraph.CohereRerank") as mock_cohere:
            mock_reranker = Mock()
            mock_cohere.return_value = mock_reranker

            reranker = rag_instance.get_reranker(
                supplier=DefaultRerankers.COHERE,
                model="rerank-v3.5",
                api_key="test-key",
            )

            mock_cohere.assert_called_once_with(
                model="rerank-v3.5", top_n=5, cohere_api_key="test-key"
            )
            assert reranker == mock_reranker

    def test_get_reranker_jina(self, rag_instance):
        """Test getting Jina reranker."""
        with patch("quivr_core.rag.quivr_rag_langgraph.JinaRerank") as mock_jina:
            mock_reranker = Mock()
            mock_jina.return_value = mock_reranker

            reranker = rag_instance.get_reranker(
                supplier=DefaultRerankers.JINA,
                model="jina-reranker-v2-base-multilingual",
                api_key="test-key",
            )

            mock_jina.assert_called_once_with(
                model="jina-reranker-v2-base-multilingual",
                top_n=5,
                jina_api_key="test-key",
            )
            assert reranker == mock_reranker

    def test_get_reranker_default(self, rag_instance):
        """Test getting default (idempotent) reranker."""
        reranker = rag_instance.get_reranker(supplier=None)

        assert isinstance(reranker, IdempotentCompressor)

    def test_get_retriever(self, rag_instance, mem_vector_store):
        """Test getting retriever from vector store."""
        retriever = rag_instance.get_retriever(search_kwargs={"k": 10})

        # The retriever should be created successfully
        assert retriever is not None

    def test_get_retriever_no_vector_store(self, simple_retrieval_config, fake_llm):
        """Test getting retriever without vector store raises error."""
        rag_instance = QuivrQARAGLangGraph(
            retrieval_config=simple_retrieval_config, llm=fake_llm, vector_store=None
        )

        with pytest.raises(ValueError, match="No vector store provided"):
            rag_instance.get_retriever()

    def test_filter_chunks_by_relevance_no_threshold(self, rag_instance):
        """Test filtering chunks when no relevance threshold is set."""
        chunks = [
            Document(
                page_content="test",
                metadata={"original_file_name": "test.pdf", "index": 0},
            )
        ]

        result = rag_instance.filter_chunks_by_relevance(chunks)

        assert result == chunks

    def test_filter_chunks_by_relevance_with_threshold(self, rag_instance):
        """Test filtering chunks with relevance threshold."""
        chunks = [
            Document(
                page_content="relevant",
                metadata={
                    "relevance_score": 0.8,
                    "original_file_name": "test1.pdf",
                    "index": 0,
                },
            ),
            Document(
                page_content="not relevant",
                metadata={
                    "relevance_score": 0.3,
                    "original_file_name": "test2.pdf",
                    "index": 1,
                },
            ),
        ]

        result = rag_instance.filter_chunks_by_relevance(
            chunks, relevance_score_threshold=0.5
        )

        assert len(result) == 1
        assert result[0].page_content == "relevant"

    @patch("quivr_core.rag.quivr_rag_langgraph.custom_prompts")
    def test_invoke_structured_output(self, mock_prompts, rag_instance):
        """Test invoke_structured_output method."""
        mock_structured_llm = Mock()
        mock_structured_llm.invoke.return_value = SplittedInput(
            instructions="test instruction", task_list=["task1", "task2"]
        )
        rag_instance.llm_endpoint._llm.with_structured_output = Mock(
            return_value=mock_structured_llm
        )

        result = rag_instance.invoke_structured_output("test prompt", SplittedInput)

        assert isinstance(result, SplittedInput)
        assert result.instructions == "test instruction"

    def test_update_active_tools_activate(self, rag_instance):
        """Test updating active tools - activation."""
        # Create mock tools
        mock_tool1 = Mock()
        mock_tool1.name = "search_tool"
        mock_tool2 = Mock()
        mock_tool2.name = "calc_tool"

        rag_instance.retrieval_config.workflow_config.validated_tools = [
            mock_tool1,
            mock_tool2,
        ]
        rag_instance.retrieval_config.workflow_config.activated_tools = []

        updated_tools = UpdatedPromptAndTools(
            tools_to_activate=["search_tool"], tools_to_deactivate=[]
        )

        rag_instance.update_active_tools(updated_tools)

        assert len(rag_instance.retrieval_config.workflow_config.activated_tools) == 1
        assert (
            rag_instance.retrieval_config.workflow_config.activated_tools[0]
            == mock_tool1
        )

    def test_update_active_tools_deactivate(self, rag_instance):
        """Test updating active tools - deactivation."""
        # Create mock tools
        mock_tool1 = Mock()
        mock_tool1.name = "search_tool"

        rag_instance.retrieval_config.workflow_config.activated_tools = [mock_tool1]

        updated_tools = UpdatedPromptAndTools(
            tools_to_activate=[], tools_to_deactivate=["search_tool"]
        )

        rag_instance.update_active_tools(updated_tools)

        assert len(rag_instance.retrieval_config.workflow_config.activated_tools) == 0

    @patch("quivr_core.rag.entities.config.WorkflowConfig.get_node_tools")
    def test_bind_tools_to_llm_with_function_calling(
        self, mock_get_node_tools, rag_instance
    ):
        """Test binding tools to LLM when function calling is supported."""
        mock_tool = Mock()
        mock_get_node_tools.return_value = [mock_tool]

        rag_instance.llm_endpoint.supports_func_calling = Mock(return_value=True)

        mock_bound_llm = Mock()
        # Replace the actual method with a Mock
        rag_instance.llm_endpoint._llm.bind_tools = Mock(return_value=mock_bound_llm)

        result = rag_instance.bind_tools_to_llm("test_node_with_tools")

        mock_get_node_tools.assert_called_once_with("test_node_with_tools")
        rag_instance.llm_endpoint._llm.bind_tools.assert_called_once_with(
            [mock_tool], tool_choice="any"
        )
        assert result == mock_bound_llm

    def test_bind_tools_to_llm_without_function_calling(self, rag_instance):
        """Test binding tools to LLM when function calling is not supported."""
        # Replace the actual method with a Mock
        rag_instance.llm_endpoint.supports_func_calling = Mock(return_value=False)

        result = rag_instance.bind_tools_to_llm("test_node")

        assert result == rag_instance.llm_endpoint._llm

    @patch("quivr_core.rag.entities.config.WorkflowConfig.get_node_tools")
    def test_bind_tools_to_llm_no_tools(self, mock_get_node_tools, rag_instance):
        """Test binding tools to LLM when no tools are available."""
        mock_get_node_tools.return_value = []

        # Replace the actual method with a Mock
        rag_instance.llm_endpoint.supports_func_calling = Mock(return_value=True)

        result = rag_instance.bind_tools_to_llm("test_node_no_tools")

        mock_get_node_tools.assert_called_once_with("test_node_no_tools")
        assert result == rag_instance.llm_endpoint._llm

    def test_filter_history(self, rag_instance):
        """Test filtering chat history."""
        brain_id = uuid4()
        chat_history = ChatHistory(chat_id=uuid4(), brain_id=brain_id)

        # Add multiple message pairs
        for i in range(5):
            chat_history.append(HumanMessage(content=f"Question {i}"))
            chat_history.append(AIMessage(content=f"Answer {i}"))

        state: AgentState = {
            "messages": [HumanMessage(content="Current question")],
            "chat_history": chat_history,
            "reasoning": [],
            "files": "",
            "tasks": UserTasks(),
            "instructions": "",
            "ticket_metadata": None,
            "user_metadata": None,
            "additional_information": None,
            "tool": "",
            "guidelines": "",
            "enforced_system_prompt": "",
            "_filter": None,
            "ticket_history": "",
        }

        # Mock token counting to allow only 2 pairs
        # Replace the actual method with a Mock
        rag_instance.llm_endpoint.count_tokens = Mock(return_value=50)
        rag_instance.retrieval_config.max_history = 2

        result = rag_instance.filter_history(state)

        # Should keep only the last 2 pairs
        filtered_history = result["chat_history"]
        assert len(list(filtered_history.iter_pairs())) <= 2

    @patch("quivr_core.rag.quivr_rag_langgraph.custom_prompts")
    async def test_rewrite(self, mock_prompts, rag_instance):
        """Test rewriting user tasks."""
        tasks = UserTasks(["Original task"])
        chat_history = ChatHistory(chat_id=uuid4(), brain_id=uuid4())

        state: AgentState = {
            "messages": [HumanMessage(content="Test question")],
            "chat_history": chat_history,
            "reasoning": [],
            "files": "",
            "tasks": tasks,
            "instructions": "",
            "ticket_metadata": None,
            "user_metadata": None,
            "additional_information": None,
            "tool": "",
            "guidelines": "",
            "enforced_system_prompt": "",
            "_filter": None,
            "ticket_history": "",
        }

        # Mock LLM response
        mock_response = Mock()
        mock_response.content = "Rewritten task"
        rag_instance.llm_endpoint._llm.ainvoke = AsyncMock(return_value=mock_response)

        # Mock the prompt template
        mock_template = Mock()
        mock_template.format.return_value = "formatted prompt"
        mock_prompts.__getitem__.return_value = mock_template

        result = await rag_instance.rewrite(state)

        # Check that task was rewritten
        updated_tasks = result["tasks"]
        assert updated_tasks.definitions[0] == "Rewritten task"

    def test_get_rag_context_length(self, rag_instance):
        """Test getting RAG context length."""
        state: AgentState = {
            "messages": [HumanMessage(content="Test question")],
            "chat_history": ChatHistory(chat_id=uuid4(), brain_id=uuid4()),
            "reasoning": [],
            "files": "test.pdf",
            "tasks": UserTasks(),
            "instructions": "",
            "ticket_metadata": None,
            "user_metadata": None,
            "additional_information": None,
            "tool": "",
            "guidelines": "",
            "enforced_system_prompt": "",
            "_filter": None,
            "ticket_history": "",
        }

        docs = [
            Document(
                page_content="test content",
                metadata={"original_file_name": "test.pdf", "index": 0},
            )
        ]

        with patch("quivr_core.rag.quivr_rag_langgraph.custom_prompts") as mock_prompts:
            mock_template = Mock()
            mock_template.format.return_value = "formatted prompt"
            mock_prompts.__getitem__.return_value = mock_template

            # Replace the actual method with a Mock
            rag_instance.llm_endpoint.count_tokens = Mock(return_value=500)

            result = rag_instance.get_rag_context_length(state, docs)

            assert result == 500

    def test_build_rag_prompt_inputs(self, rag_instance):
        """Test building RAG prompt inputs."""
        tasks = UserTasks(["Test task"])
        chat_history = ChatHistory(chat_id=uuid4(), brain_id=uuid4())

        state: AgentState = {
            "messages": [HumanMessage(content="Test question")],
            "chat_history": chat_history,
            "reasoning": [],
            "files": "test.pdf",
            "tasks": tasks,
            "instructions": "",
            "ticket_metadata": None,
            "user_metadata": None,
            "additional_information": None,
            "tool": "",
            "guidelines": "",
            "enforced_system_prompt": "",
            "_filter": None,
            "ticket_history": "",
        }

        docs = [
            Document(
                page_content="test content",
                metadata={"original_file_name": "test.pdf", "index": 0},
            )
        ]

        with patch(
            "quivr_core.rag.quivr_rag_langgraph.combine_documents"
        ) as mock_combine:
            mock_combine.return_value = "combined docs"

            result = rag_instance._build_rag_prompt_inputs(state, docs)

            expected_keys = {
                "context",
                "task",
                "rephrased_task",
                "custom_instructions",
                "files",
                "chat_history",
            }
            assert set(result.keys()) == expected_keys
            assert result["task"] == "Test question"
            assert result["files"] == "test.pdf"
            assert result["context"] == "combined docs"

    @patch("quivr_core.rag.quivr_rag_langgraph.custom_prompts")
    def test_generate_rag(self, mock_prompts, rag_instance):
        """Test generating RAG response."""
        tasks = UserTasks(["Test task"])
        docs = [
            Document(
                page_content="test content",
                metadata={"original_file_name": "test.pdf", "index": 0},
            )
        ]
        tasks.set_docs(tasks.ids[0], docs)

        state: AgentState = {
            "messages": [HumanMessage(content="Test question")],
            "chat_history": ChatHistory(chat_id=uuid4(), brain_id=uuid4()),
            "reasoning": [],
            "files": "test.pdf",
            "tasks": tasks,
            "instructions": "",
            "ticket_metadata": None,
            "user_metadata": None,
            "additional_information": None,
            "tool": "",
            "guidelines": "",
            "enforced_system_prompt": "",
            "_filter": None,
            "ticket_history": "",
        }

        # Mock prompt template
        mock_template = Mock()
        mock_template.format.return_value = "formatted prompt"
        mock_prompts.__getitem__.return_value = mock_template

        # Mock LLM response
        mock_response = AIMessage(content="Generated answer")

        with patch.object(rag_instance, "bind_tools_to_llm") as mock_bind_tools:
            mock_llm = Mock()
            mock_llm.invoke.return_value = mock_response
            mock_bind_tools.return_value = mock_llm

            with patch.object(
                rag_instance, "reduce_rag_context", return_value=(state, {})
            ):
                result = rag_instance.generate_rag(state)

                assert "messages" in result
                assert len(result["messages"]) == 1
                assert result["messages"][0] == mock_response

    def test_create_graph(self, rag_instance):
        """Test creating the workflow graph."""
        with patch.object(rag_instance, "_build_workflow") as mock_build:
            graph = rag_instance.create_graph()

            assert graph is not None
            mock_build.assert_called_once()

    def test_build_chain(self, rag_instance):
        """Test building the chain."""
        with patch.object(rag_instance, "create_graph") as mock_create:
            mock_graph = Mock()
            mock_create.return_value = mock_graph

            chain = rag_instance.build_chain()

            assert chain == mock_graph
            assert rag_instance.graph == mock_graph

    def test_build_chain_existing_graph(self, rag_instance):
        """Test building chain when graph already exists."""
        existing_graph = Mock()
        rag_instance.graph = existing_graph

        chain = rag_instance.build_chain()

        assert chain == existing_graph


class TestStreamingHelpers:
    """Test streaming helper methods."""

    @pytest.fixture
    def rag_instance(self, simple_retrieval_config, fake_llm, mem_vector_store):
        """Create a QuivrQARAGLangGraph instance."""
        return QuivrQARAGLangGraph(
            retrieval_config=simple_retrieval_config,
            llm=fake_llm,
            vector_store=mem_vector_store,
        )

    @pytest.fixture
    def simple_retrieval_config(self):
        """Create a retrieval config with final nodes."""
        with patch.dict("os.environ", {}, clear=True):
            return RetrievalConfig(
                llm_config=LLMEndpointConfig(
                    model="gpt-4o", max_context_tokens=128000, max_output_tokens=4096
                ),
                workflow_config=WorkflowConfig(
                    nodes=[
                        NodeConfig(name=START, edges=["generate_rag"]),
                        NodeConfig(name="generate_rag", edges=[END]),
                    ]
                ),
            )

    def test_is_final_node_with_docs(self, rag_instance):
        """Test _is_final_node_with_docs method."""
        # Set up final nodes
        rag_instance.final_nodes = ["generate_rag"]

        # Valid event with docs
        event = {
            "data": {"output": {"tasks": UserTasks(["test task"])}},
            "metadata": {"langgraph_node": "generate_rag"},
        }

        assert rag_instance._is_final_node_with_docs(event)

        # Invalid event - not final node
        event["metadata"]["langgraph_node"] = "other_node"
        assert not rag_instance._is_final_node_with_docs(event)

        # Invalid event - no output
        event["metadata"]["langgraph_node"] = "generate_rag"
        event["data"]["output"] = None
        assert not rag_instance._is_final_node_with_docs(event)

    def test_is_final_node_and_chat_model_stream(self, rag_instance):
        """Test _is_final_node_and_chat_model_stream method."""
        # Set up final nodes
        rag_instance.final_nodes = ["generate_rag"]

        # Valid streaming event
        event = {
            "event": "on_chat_model_stream",
            "metadata": {"langgraph_node": "generate_rag"},
        }

        assert rag_instance._is_final_node_and_chat_model_stream(event)

        # Invalid event - wrong event type
        event["event"] = "on_llm_start"
        assert not rag_instance._is_final_node_and_chat_model_stream(event)

        # Invalid event - not final node
        event["event"] = "on_chat_model_stream"
        event["metadata"]["langgraph_node"] = "other_node"
        assert not rag_instance._is_final_node_and_chat_model_stream(event)

    def test_extract_node_name(self, rag_instance):
        """Test _extract_node_name method."""
        # Event with metadata
        event = {"metadata": {"langgraph_node": "generate_rag"}}

        # No description, should return node name
        result = rag_instance._extract_node_name(event)
        assert result == "generate_rag"

        # With description
        rag_instance.retrieval_config.workflow_config.nodes[
            1
        ].description = "Generate Answer"
        result = rag_instance._extract_node_name(event)
        assert result == "Generate Answer"

        # Event without metadata
        event = {}
        result = rag_instance._extract_node_name(event)
        assert result == ""


class TestDataModels:
    """Test Pydantic data models."""

    def test_splitted_input(self):
        """Test SplittedInput model."""
        input_data = SplittedInput(
            instructions_reasoning="This is reasoning",
            instructions="Do this task",
            tasks_reasoning="These are tasks",
            task_list=["Task 1", "Task 2"],
        )

        assert input_data.instructions_reasoning == "This is reasoning"
        assert input_data.instructions == "Do this task"
        assert input_data.task_list == ["Task 1", "Task 2"]

    def test_splitted_input_defaults(self):
        """Test SplittedInput with default values."""
        input_data = SplittedInput()

        assert input_data.instructions_reasoning is None
        assert input_data.instructions is None
        assert input_data.task_list == ["No explicit or implicit tasks found"]

    def test_tasks_completion(self):
        """Test TasksCompletion model."""
        completion = TasksCompletion(
            is_task_completable_reasoning="Can be completed",
            is_task_completable=True,
            tool_reasoning="Use search tool",
            tool="search_tool",
        )

        assert completion.is_task_completable is True
        assert completion.tool == "search_tool"

    def test_final_answer(self):
        """Test FinalAnswer model."""
        answer = FinalAnswer(
            reasoning_answer="Step by step reasoning",
            answer="Final answer text",
            all_tasks_completed=True,
        )

        assert answer.reasoning_answer == "Step by step reasoning"
        assert answer.answer == "Final answer text"
        assert answer.all_tasks_completed is True

    def test_updated_prompt_and_tools(self):
        """Test UpdatedPromptAndTools model."""
        update = UpdatedPromptAndTools(
            prompt_reasoning="Updated reasoning",
            prompt="New prompt",
            tools_reasoning="Tool reasoning",
            tools_to_activate=["tool1"],
            tools_to_deactivate=["tool2"],
        )

        assert update.prompt == "New prompt"
        assert update.tools_to_activate == ["tool1"]
        assert update.tools_to_deactivate == ["tool2"]

    def test_updated_prompt_and_tools_defaults(self):
        """Test UpdatedPromptAndTools with defaults."""
        update = UpdatedPromptAndTools()

        assert update.tools_to_activate == []
        assert update.tools_to_deactivate == []


@pytest.mark.asyncio
class TestAsyncMethods:
    """Test asynchronous methods."""

    @pytest.fixture
    def rag_instance(self, simple_retrieval_config, fake_llm, mem_vector_store):
        """Create a QuivrQARAGLangGraph instance."""
        return QuivrQARAGLangGraph(
            retrieval_config=simple_retrieval_config,
            llm=fake_llm,
            vector_store=mem_vector_store,
        )

    @pytest.fixture
    def simple_retrieval_config(self):
        """Create a basic retrieval config."""
        with patch.dict("os.environ", {}, clear=True):
            return RetrievalConfig(
                llm_config=LLMEndpointConfig(
                    model="gpt-4o", max_context_tokens=128000, max_output_tokens=4096
                ),
                workflow_config=WorkflowConfig(
                    nodes=[
                        NodeConfig(name=START, edges=["retrieve"]),
                        NodeConfig(name="retrieve", edges=[END]),
                    ]
                ),
            )

    async def test_retrieve(self, rag_instance):
        """Test retrieve method."""
        tasks = UserTasks(["Test task"])
        state: AgentState = {
            "messages": [HumanMessage(content="Test question")],
            "chat_history": ChatHistory(chat_id=uuid4(), brain_id=uuid4()),
            "reasoning": [],
            "files": "",
            "tasks": tasks,
            "instructions": "",
            "ticket_metadata": None,
            "user_metadata": None,
            "additional_information": None,
            "tool": "",
            "guidelines": "",
            "enforced_system_prompt": "",
            "_filter": None,
            "ticket_history": "",
        }

        # Mock retriever
        mock_docs = [
            Document(
                page_content="test",
                metadata={
                    "relevance_score": 0.8,
                    "original_file_name": "test.pdf",
                    "index": 0,
                },
            )
        ]
        mock_retriever = Mock()
        mock_retriever.ainvoke = AsyncMock(return_value=mock_docs)

        with patch.object(
            rag_instance, "get_retriever", return_value=mock_retriever
        ), patch.object(
            rag_instance, "get_reranker", return_value=IdempotentCompressor()
        ), patch(
            "quivr_core.rag.quivr_rag_langgraph.ContextualCompressionRetriever"
        ) as mock_compression:
            mock_compression_instance = Mock()
            mock_compression_instance.ainvoke = AsyncMock(return_value=mock_docs)
            mock_compression.return_value = mock_compression_instance

            result = await rag_instance.retrieve(state)

            # Check that docs were set for the task
            updated_tasks = result["tasks"]
            assert len(updated_tasks(tasks.ids[0]).docs) > 0

    async def test_tool_routing(self, rag_instance):
        """Test tool_routing method."""
        tasks = UserTasks(["Test task"])
        docs = [
            Document(
                page_content="context",
                metadata={"original_file_name": "test.pdf", "index": 0},
            )
        ]
        tasks.set_docs(tasks.ids[0], docs)

        state: AgentState = {
            "messages": [HumanMessage(content="Test question")],
            "chat_history": ChatHistory(chat_id=uuid4(), brain_id=uuid4()),
            "reasoning": [],
            "files": "",
            "tasks": tasks,
            "instructions": "",
            "ticket_metadata": None,
            "user_metadata": None,
            "additional_information": None,
            "tool": "",
            "guidelines": "",
            "enforced_system_prompt": "",
            "_filter": None,
            "ticket_history": "",
        }

        # Mock structured output
        completion_response = TasksCompletion(is_task_completable=True, tool=None)

        with patch.object(
            rag_instance, "ainvoke_structured_output", return_value=completion_response
        ), patch(
            "quivr_core.rag.quivr_rag_langgraph.collect_tools",
            return_value=("available", "activated"),
        ), patch("quivr_core.rag.quivr_rag_langgraph.custom_prompts") as mock_prompts:
            mock_template = Mock()
            mock_template.format.return_value = "formatted prompt"
            mock_prompts.__getitem__.return_value = mock_template

            result = await rag_instance.tool_routing(state)

            # Should route to generate_rag since task is completable
            assert len(result) == 1
            assert result[0].node == "generate_rag"


# Integration test to ensure all components work together
@pytest.mark.asyncio
class TestIntegration:
    """Integration tests for the RAG system."""

    @pytest.fixture
    def full_retrieval_config(self):
        """Create a full retrieval config."""
        with patch.dict("os.environ", {}, clear=True):
            return RetrievalConfig(
                llm_config=LLMEndpointConfig(
                    model="gpt-4o", max_context_tokens=128000, max_output_tokens=4096
                ),
                reranker_config=RerankerConfig(),
                workflow_config=WorkflowConfig(
                    nodes=[
                        NodeConfig(name=START, edges=["filter_history"]),
                        NodeConfig(name="filter_history", edges=["retrieve"]),
                        NodeConfig(name="retrieve", edges=["generate_rag"]),
                        NodeConfig(name="generate_rag", edges=[END]),
                    ]
                ),
            )

    async def test_full_workflow_creation(
        self, full_retrieval_config, fake_llm, mem_vector_store
    ):
        """Test creating a full workflow with multiple nodes."""
        rag = QuivrQARAGLangGraph(
            retrieval_config=full_retrieval_config,
            llm=fake_llm,
            vector_store=mem_vector_store,
        )

        # Should be able to create graph without errors
        graph = rag.create_graph()
        assert graph is not None

        # Should have final nodes identified
        assert len(rag.final_nodes) > 0
