from unittest.mock import MagicMock, patch

from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_openai import AzureOpenAIEmbeddings
from quivr_api.modules.dependencies import get_embedding_client


def test_ollama_embedding():
    with patch("quivr_api.modules.dependencies.settings") as mock_settings:
        mock_settings.ollama_api_base_url = "http://ollama.example.com"
        mock_settings.azure_openai_embeddings_url = None

        embedding_client = get_embedding_client()

        assert isinstance(embedding_client, OllamaEmbeddings)
        assert embedding_client.base_url == "http://ollama.example.com"


def test_azure_embedding():
    with patch("quivr_api.modules.dependencies.settings") as mock_settings:
        mock_settings.ollama_api_base_url = None
        mock_settings.azure_openai_embeddings_url = "https://quivr-test.openai.azure.com/openai/deployments/embedding/embeddings?api-version=2023-05-15"

        embedding_client = get_embedding_client()

        assert isinstance(embedding_client, AzureOpenAIEmbeddings)
        assert embedding_client.azure_endpoint == "https://quivr-test.openai.azure.com"


def test_openai_embedding():
    with (
        patch("quivr_api.modules.dependencies.settings") as mock_settings,
        patch(
            "quivr_api.modules.dependencies.OpenAIEmbeddings"
        ) as mock_openai_embeddings,
    ):
        mock_settings.ollama_api_base_url = None
        mock_settings.azure_openai_embeddings_url = None

        # Create a mock instance for OpenAIEmbeddings
        mock_openai_instance = MagicMock()
        mock_openai_embeddings.return_value = mock_openai_instance

        embedding_client = get_embedding_client()

        assert embedding_client == mock_openai_instance
