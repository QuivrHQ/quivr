"""Tests for the LLM service."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
import openai
from pydantic import BaseModel

from quivr_core.rag.entities.config import LLMEndpointConfig
from quivr_core.rag.langgraph_framework.services.llm_service import LLMService
from quivr_core.llm import LLMEndpoint


class SampleOutputModel(BaseModel):
    """Sample Pydantic model for structured output testing."""

    response: str
    confidence: float


class TestLLMServiceInitialization:
    """Test LLM service initialization."""

    def test_initialization_with_config(self):
        """Test LLM service initialization with config."""
        config = LLMEndpointConfig(
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_context_tokens=12000,
            max_output_tokens=8000,
        )

        with patch.object(LLMEndpoint, "from_config") as mock_from_config:
            mock_endpoint = Mock()
            mock_from_config.return_value = mock_endpoint

            service = LLMService(config)

            assert service.config == config
            assert service.llm_endpoint == mock_endpoint
            mock_from_config.assert_called_once_with(config)


class TestLLMServiceInvoke:
    """Test LLM service invoke methods."""

    @pytest.fixture(scope="function")
    def mock_llm_service(self):
        """Create a mock LLM service."""
        config = LLMEndpointConfig()

        with patch.object(LLMEndpoint, "from_config") as mock_from_config:
            mock_endpoint = Mock()
            mock_llm = Mock()
            mock_llm.ainvoke = AsyncMock()
            mock_endpoint._llm = mock_llm
            mock_from_config.return_value = mock_endpoint

            service = LLMService(config)
            return service, mock_llm

    @pytest.mark.asyncio(loop_scope="session")
    async def test_invoke_basic(self, mock_llm_service):
        """Test basic LLM invocation."""
        service, mock_llm = mock_llm_service
        mock_llm.ainvoke.return_value = "Test response"

        result = await service.invoke("Test prompt")

        assert result == "Test response"
        mock_llm.ainvoke.assert_called_once_with("Test prompt")

    @pytest.mark.asyncio(loop_scope="session")
    async def test_invoke_with_structured_output_json_schema(self, mock_llm_service):
        """Test structured output with JSON schema method."""
        service, mock_llm = mock_llm_service

        # Create a mock structured LLM with proper async method
        mock_structured_llm = Mock()
        mock_structured_llm.ainvoke = AsyncMock(
            return_value=SampleOutputModel(response="Test response", confidence=0.95)
        )

        # Mock the with_structured_output method
        mock_llm.with_structured_output.return_value = mock_structured_llm

        result = await service.invoke_with_structured_output(
            "Test prompt", SampleOutputModel
        )

        assert isinstance(result, SampleOutputModel)
        assert result.response == "Test response"
        assert result.confidence == 0.95

        mock_llm.with_structured_output.assert_called_once_with(
            SampleOutputModel, method="json_schema"
        )
        mock_structured_llm.ainvoke.assert_called_once_with("Test prompt")

    @pytest.mark.asyncio(loop_scope="session")
    async def test_invoke_with_structured_output_fallback(self, mock_llm_service):
        """Test structured output fallback when JSON schema fails."""
        service, mock_llm = mock_llm_service

        # Create mock for fallback structured LLM
        mock_fallback_llm = Mock()
        mock_fallback_llm.ainvoke = AsyncMock(
            return_value=SampleOutputModel(response="Fallback response", confidence=0.8)
        )

        # First call raises BadRequestError, second call returns fallback mock
        mock_llm.with_structured_output.side_effect = [
            openai.BadRequestError(
                "JSON schema not supported", response=Mock(), body={}
            ),
            mock_fallback_llm,
        ]

        with patch(
            "quivr_core.rag.langgraph_framework.services.llm_service.logger"
        ) as mock_logger:
            result = await service.invoke_with_structured_output(
                "Test prompt", SampleOutputModel
            )

        assert isinstance(result, SampleOutputModel)
        assert result.response == "Fallback response"

        # Should have called with_structured_output twice
        assert mock_llm.with_structured_output.call_count == 2
        mock_logger.warning.assert_called_once()

    def test_invoke_with_structured_output_sync(self, mock_llm_service):
        """Test synchronous structured output."""
        service, mock_llm = mock_llm_service

        # Create mock structured LLM with sync method
        mock_structured_llm = Mock()
        mock_structured_llm.invoke.return_value = SampleOutputModel(
            response="Sync response", confidence=0.9
        )

        mock_llm.with_structured_output.return_value = mock_structured_llm

        result = service.invoke_with_structured_output_sync(
            "Test prompt", SampleOutputModel
        )

        assert isinstance(result, SampleOutputModel)
        assert result.response == "Sync response"
        mock_structured_llm.invoke.assert_called_once_with("Test prompt")

    def test_invoke_with_structured_output_sync_fallback(self, mock_llm_service):
        """Test synchronous structured output fallback."""
        service, mock_llm = mock_llm_service

        # Create mock for fallback
        mock_fallback_llm = Mock()
        mock_fallback_llm.invoke.return_value = SampleOutputModel(
            response="Sync fallback", confidence=0.85
        )

        mock_llm.with_structured_output.side_effect = [
            openai.BadRequestError(
                "JSON schema not supported", response=Mock(), body={}
            ),
            mock_fallback_llm,
        ]

        result = service.invoke_with_structured_output_sync(
            "Test prompt", SampleOutputModel
        )

        assert result.response == "Sync fallback"
        assert mock_llm.with_structured_output.call_count == 2


class TestLLMServiceTokenCounting:
    """Test token counting functionality."""

    @pytest.fixture(scope="function")
    def mock_llm_service_with_tokenizer(self):
        """Create mock LLM service with tokenizer."""
        config = LLMEndpointConfig()

        with patch.object(LLMEndpoint, "from_config") as mock_from_config:
            mock_endpoint = Mock()
            mock_endpoint.count_tokens.return_value = 42
            mock_from_config.return_value = mock_endpoint

            service = LLMService(config)
            return service, mock_endpoint

    def test_count_tokens(self, mock_llm_service_with_tokenizer):
        """Test token counting."""
        service, mock_endpoint = mock_llm_service_with_tokenizer

        result = service.count_tokens("This is a test string")

        assert result == 42
        mock_endpoint.count_tokens.assert_called_once_with("This is a test string")


class TestLLMServiceConfiguration:
    """Test configuration-related methods."""

    def test_supports_function_calling(self):
        """Test function calling support check."""
        config = LLMEndpointConfig()

        with patch.object(LLMEndpoint, "from_config") as mock_from_config:
            mock_endpoint = Mock()
            mock_endpoint.supports_func_calling.return_value = True
            mock_from_config.return_value = mock_endpoint

            service = LLMService(config)

            assert service.supports_function_calling() is True
            mock_endpoint.supports_func_calling.assert_called_once()

    def test_get_max_context_tokens(self):
        """Test getting max context tokens."""
        config = LLMEndpointConfig(max_context_tokens=8000)

        with patch.object(LLMEndpoint, "from_config"):
            service = LLMService(config)

            assert service.get_max_context_tokens() == 8000

    def test_get_max_output_tokens(self):
        """Test getting max output tokens."""
        config = LLMEndpointConfig(max_output_tokens=8000)

        with patch.object(LLMEndpoint, "from_config"):
            service = LLMService(config)

            assert service.get_max_output_tokens() == 8000


class TestLLMServiceErrorHandling:
    """Test error handling in LLM service."""

    @pytest.mark.asyncio(loop_scope="session")
    async def test_invoke_with_llm_error(self):
        """Test handling of LLM errors during invocation."""
        config = LLMEndpointConfig()

        with patch.object(LLMEndpoint, "from_config") as mock_from_config:
            mock_endpoint = Mock()
            mock_llm = Mock()
            mock_llm.ainvoke = AsyncMock(side_effect=Exception("LLM error"))
            mock_endpoint._llm = mock_llm
            mock_from_config.return_value = mock_endpoint

            service = LLMService(config)

            with pytest.raises(Exception, match="LLM error"):
                await service.invoke("Test prompt")

    @pytest.mark.asyncio(loop_scope="session")
    async def test_structured_output_with_invalid_model_class(self):
        """Test structured output with invalid model class."""
        config = LLMEndpointConfig()

        with patch.object(LLMEndpoint, "from_config") as mock_from_config:
            mock_endpoint = Mock()
            mock_llm = Mock()

            # Mock structured LLM that raises an error
            mock_structured_llm = Mock()
            mock_structured_llm.ainvoke = AsyncMock(
                side_effect=ValueError("Invalid model")
            )
            mock_llm.with_structured_output.return_value = mock_structured_llm

            mock_endpoint._llm = mock_llm
            mock_from_config.return_value = mock_endpoint

            service = LLMService(config)

            with pytest.raises(ValueError, match="Invalid model"):
                await service.invoke_with_structured_output(
                    "Test prompt", SampleOutputModel
                )


class TestLLMServiceEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_count_tokens_with_empty_string(self):
        """Test token counting with empty string."""
        config = LLMEndpointConfig()

        with patch.object(LLMEndpoint, "from_config") as mock_from_config:
            mock_endpoint = Mock()
            mock_endpoint.count_tokens.return_value = 0
            mock_from_config.return_value = mock_endpoint

            service = LLMService(config)

            result = service.count_tokens("")

            assert result == 0
            mock_endpoint.count_tokens.assert_called_once_with("")

    def test_count_tokens_with_very_long_text(self):
        """Test token counting with very long text."""
        config = LLMEndpointConfig()

        with patch.object(LLMEndpoint, "from_config") as mock_from_config:
            mock_endpoint = Mock()
            mock_endpoint.count_tokens.return_value = 10000
            mock_from_config.return_value = mock_endpoint

            service = LLMService(config)
            long_text = "word " * 5000  # Very long text

            result = service.count_tokens(long_text)

            assert result == 10000
            mock_endpoint.count_tokens.assert_called_once_with(long_text)
