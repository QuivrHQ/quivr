# LangGraph Framework Unit Testing Strategy

## Overview

This document outlines a comprehensive unit testing strategy for the `quivr_core.rag.langgraph_framework` module. The framework implements a plugin-based architecture for building LangGraph workflows with dependency injection, state management, and dynamic node registration.

## Architecture Analysis

### Core Components to Test

1. **Graph Builder System** (`graph_builder.py`)
2. **State Management** (`state.py`)
3. **Task Management** (`task.py`)
4. **Utility Functions** (`utils.py`)
5. **Registry System** (`registry/node_registry.py`)
6. **Service Container** (`services/service_container.py`)
7. **Individual Services** (`services/`)
8. **Base Node System** (`nodes/base/`)
9. **Concrete Node Implementations** (`nodes/`)

## Testing Strategy

### 1. Unit Test Structure

```
tests/rag/langgraph_framework/
├── test_graph_builder.py
├── test_state.py
├── test_task.py
├── test_utils.py
├── registry/
│   └── test_node_registry.py
├── services/
│   ├── test_service_container.py
│   ├── test_llm_service.py
│   ├── test_tool_service.py
│   └── test_rag_prompt_service.py
├── nodes/
│   ├── base/
│   │   ├── test_base_node.py
│   │   ├── test_extractors.py
│   │   └── test_utils.py
│   ├── test_history_nodes.py
│   ├── test_generation_nodes.py
│   ├── test_routing_nodes.py
│   ├── test_retrieval_nodes.py
│   ├── test_task_nodes.py
│   ├── test_tool_nodes.py
│   └── test_various_nodes.py
├── integration/
│   ├── test_full_workflow.py
│   └── test_node_communication.py
└── fixtures/
    ├── mock_nodes.py
    ├── mock_services.py
    └── test_data.py
```

### 2. Testing Priorities

#### High Priority (Core Foundation)
1. **Registry System** - Critical for plugin architecture
2. **Service Container** - Essential for dependency injection
3. **Base Node** - Foundation for all nodes
4. **Graph Builder** - Core workflow construction
5. **State Management** - Data flow between nodes

#### Medium Priority (Business Logic)
1. **Task Management** - User task tracking
2. **Utility Functions** - Context reduction, tool binding
3. **Individual Services** - LLM, Tool, Prompt services
4. **Node Implementations** - Specific business logic

#### Low Priority (Integration)
1. **End-to-end Workflows** - Full pipeline testing
2. **Performance Testing** - Resource usage, timing
3. **Error Recovery** - Resilience testing

### 3. Test Categories

#### 3.1 Registry System Tests (`test_node_registry.py`)

**Test Coverage:**
- Node registration and discovery
- Category management
- Metadata handling
- Decorator functionality
- Error handling for duplicate registrations
- Node instantiation with parameters

**Key Test Cases:**
```python
def test_register_node_basic()
def test_register_node_with_metadata()
def test_register_node_duplicate_override()
def test_list_nodes_by_category()
def test_create_node_with_kwargs()
def test_node_not_found_error()
def test_decorator_registration()
def test_metadata_storage()
```

#### 3.2 Service Container Tests (`test_service_container.py`)

**Test Coverage:**
- Service registration and retrieval
- Factory pattern implementation
- Singleton behavior
- Configuration change detection
- Service lifecycle management
- Error handling for missing services

**Key Test Cases:**
```python
def test_singleton_service_creation()
def test_service_with_config()
def test_config_change_detection()
def test_service_factory_registration()
def test_invalid_service_type()
def test_cache_clearing()
def test_concurrent_access()
```

#### 3.3 Base Node Tests (`test_base_node.py`)

**Test Coverage:**
- Abstract base class functionality
- Configuration extraction and caching
- Service injection
- Error handling and validation
- State validation (input/output)
- Execution lifecycle

**Key Test Cases:**
```python
def test_node_initialization()
def test_config_extraction()
def test_config_change_detection()
def test_service_injection()
def test_input_validation()
def test_output_validation()
def test_error_handling()
def test_execution_lifecycle()
```

#### 3.4 Graph Builder Tests (`test_graph_builder.py`)

**Test Coverage:**
- Node addition and configuration
- Edge creation (simple and conditional)
- Entry/exit point setting
- Graph compilation
- Builder pattern chaining
- Error handling for invalid nodes

**Key Test Cases:**
```python
def test_add_node_success()
def test_add_node_invalid_type()
def test_add_edge()
def test_add_conditional_edge()
def test_set_entry_point()
def test_set_finish_point()
def test_builder_chaining()
def test_graph_compilation()
def test_list_available_nodes()
```

#### 3.5 State Management Tests (`test_state.py`)

**Test Coverage:**
- State model validation
- Type checking and serialization
- Default value handling
- State transitions
- Message handling with annotations

**Key Test Cases:**
```python
def test_agent_state_creation()
def test_tasks_completion_model()
def test_final_answer_model()
def test_updated_prompt_and_tools_model()
def test_idempotent_compressor()
def test_state_serialization()
```

#### 3.6 Task Management Tests (`test_task.py`)

**Test Coverage:**
- Task creation and management
- Document association
- Completion tracking
- Tool assignment
- Task iteration and properties

**Key Test Cases:**
```python
def test_user_task_entity_creation()
def test_user_tasks_initialization()
def test_set_docs()
def test_set_completion()
def test_set_tool()
def test_task_iteration()
def test_completable_tasks_property()
def test_non_completable_tasks_property()
def test_task_not_found_error()
```

#### 3.7 Utility Functions Tests (`test_utils.py`)

**Test Coverage:**
- Context length calculation
- Context reduction algorithms
- Tool activation/deactivation
- Token counting
- Document processing

**Key Test Cases:**
```python
def test_update_active_tools()
def test_get_rag_context_length()
def test_reduce_rag_context()
def test_bind_tools_to_llm()
def test_context_reduction_iteration_limit()
def test_token_counting_accuracy()
```

#### 3.8 Individual Service Tests

**LLM Service Tests (`test_llm_service.py`):**
- Service initialization
- LLM endpoint configuration
- Function calling support
- Error handling

**Tool Service Tests (`test_tool_service.py`):**
- Tool management
- Node-specific tool binding
- Tool activation/deactivation
- Workflow configuration

**Prompt Service Tests (`test_rag_prompt_service.py`):**
- Prompt template management
- Template resolution
- Context injection

#### 3.9 Node Implementation Tests

**Strategy:** Create focused tests for each node category
- Mock external dependencies (LLM calls, retrieval systems)
- Test core business logic
- Validate input/output transformations
- Error handling and edge cases

### 4. Testing Utilities and Fixtures

#### 4.1 Mock Objects (`fixtures/mock_nodes.py`)

```python
class MockNode(BaseNode):
    """Simple mock node for testing"""

class MockLLMService:
    """Mock LLM service for testing"""

class MockToolService:
    """Mock tool service for testing"""
```

#### 4.2 Test Data (`fixtures/test_data.py`)

```python
SAMPLE_AGENT_STATE = {...}
SAMPLE_USER_TASKS = {...}
SAMPLE_DOCUMENTS = {...}
SAMPLE_CHAT_HISTORY = {...}
```

#### 4.3 Common Test Utilities (`fixtures/test_utils.py`)

```python
def create_test_registry():
    """Create a registry with test nodes"""

def create_mock_graph_builder():
    """Create a graph builder with mocked dependencies"""

def assert_state_valid(state):
    """Validate state structure"""
```

### 5. Testing Patterns and Best Practices

#### 5.1 Dependency Injection Testing
- Use mock services for unit tests
- Test service container configuration
- Validate service lifecycle management

#### 5.2 Async Testing
- Use pytest-asyncio for async node testing
- Mock async dependencies appropriately
- Test concurrent execution scenarios

#### 5.3 Configuration Testing
- Test configuration extraction and validation
- Verify configuration change detection
- Test default configuration behavior

#### 5.4 Error Handling Testing
- Test all error paths and edge cases
- Validate error message clarity
- Test error recovery mechanisms

#### 5.5 State Management Testing
- Test state transitions and validation
- Verify type safety and serialization
- Test state persistence across node executions

### 6. Integration Testing Strategy

#### 6.1 Workflow Integration Tests
- Test complete workflow execution
- Validate node communication
- Test state propagation through pipeline

#### 6.2 Registry Integration Tests
- Test node discovery and instantiation
- Validate plugin loading
- Test metadata propagation

### 7. Performance and Load Testing

#### 7.1 Performance Benchmarks
- Node execution time
- Memory usage patterns
- Configuration extraction overhead

#### 7.2 Load Testing
- Concurrent workflow execution
- Service container under load
- Registry performance with many nodes

### 8. Test Data Management

#### 8.1 Test Data Strategy
- Use factories for test data generation
- Maintain separate test data for each component
- Version test data for reproducibility

#### 8.2 Fixture Management
- Shared fixtures for common objects
- Scoped fixtures for different test levels
- Cleanup strategies for test isolation

### 9. Continuous Integration Requirements

#### 9.1 Test Coverage Goals
- Minimum 90% line coverage for core components
- Minimum 80% branch coverage
- 100% coverage for critical paths (registry, service container)

#### 9.2 Test Performance Requirements
- Unit tests should complete in < 10 seconds
- Integration tests should complete in < 30 seconds
- Full test suite should complete in < 2 minutes

### 10. Test Implementation Phases

#### Phase 1: Foundation (Week 1-2)
1. Registry system tests
2. Service container tests
3. Base node tests
4. Basic utility tests

#### Phase 2: Core Components (Week 3-4)
1. Graph builder tests
2. State management tests
3. Task management tests
4. Individual service tests

#### Phase 3: Node Implementations (Week 5-6)
1. Node category tests
2. Business logic validation
3. Error handling tests

#### Phase 4: Integration (Week 7-8)
1. Workflow integration tests
2. Performance testing
3. Load testing
4. Documentation and cleanup

### 11. Maintenance Strategy

#### 11.1 Test Maintenance
- Regular review of test coverage
- Update tests for new features
- Refactor tests for maintainability

#### 11.2 Test Documentation
- Document test patterns and conventions
- Maintain test data documentation
- Update testing strategy as framework evolves

## Conclusion

This comprehensive testing strategy ensures robust coverage of the LangGraph framework's complex architecture. The multi-layered approach (unit → integration → performance) provides confidence in the system's reliability while maintaining development velocity through fast-running unit tests.

The plugin-based architecture requires special attention to the registry system and dependency injection, which are critical for the framework's extensibility. The testing strategy addresses these concerns through focused testing of core components and comprehensive mocking strategies.
