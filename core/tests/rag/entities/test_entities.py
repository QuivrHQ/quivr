import datetime
from uuid import uuid4

import pytest
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import ValidationError

from quivr_core.rag.entities.models import (
    cited_answer,
    ChatMessage,
    KnowledgeStatus,
    Source,
    RawRAGChunkResponse,
    RawRAGResponse,
    ChatLLMMetadata,
    RAGResponseMetadata,
    ParsedRAGResponse,
    ParsedRAGChunkResponse,
    QuivrKnowledge,
    SearchResult,
)


class TestCitedAnswerModel:
    """Test the cited_answer Pydantic model."""

    def test_cited_answer_creation(self):
        """Test creating a cited_answer instance."""
        answer = cited_answer(
            answer="This is the answer",
            citations=[1, 2, 3],
            followup_questions=["What about X?", "How does Y work?"],
        )

        assert answer.answer == "This is the answer"
        assert answer.citations == [1, 2, 3]
        assert answer.followup_questions == ["What about X?", "How does Y work?"]

    def test_cited_answer_validation(self):
        """Test validation of cited_answer fields."""
        # Test missing required fields
        with pytest.raises(ValidationError):
            cited_answer()

        with pytest.raises(ValidationError):
            cited_answer(answer="test")  # Missing citations and followup_questions

    def test_cited_answer_empty_lists(self):
        """Test cited_answer with empty lists."""
        answer = cited_answer(answer="Test answer", citations=[], followup_questions=[])

        assert answer.citations == []
        assert answer.followup_questions == []

    def test_cited_answer_field_descriptions(self):
        """Test that cited_answer has proper field descriptions."""
        model_fields = cited_answer.model_fields

        assert "answer" in model_fields
        assert "citations" in model_fields
        assert "followup_questions" in model_fields

        # Check that descriptions exist
        assert model_fields["answer"].description is not None
        assert model_fields["citations"].description is not None
        assert model_fields["followup_questions"].description is not None


class TestChatMessage:
    """Test the ChatMessage model."""

    def test_chat_message_creation_human(self):
        """Test creating a ChatMessage with HumanMessage."""
        chat_id = uuid4()
        message_id = uuid4()
        brain_id = uuid4()
        msg = HumanMessage(content="Hello")
        now = datetime.datetime.now()

        chat_message = ChatMessage(
            chat_id=chat_id,
            message_id=message_id,
            brain_id=brain_id,
            msg=msg,
            message_time=now,
            metadata={"source": "user"},
        )

        assert chat_message.chat_id == chat_id
        assert chat_message.message_id == message_id
        assert chat_message.brain_id == brain_id
        assert chat_message.msg == msg
        assert chat_message.message_time == now
        assert chat_message.metadata == {"source": "user"}

    def test_chat_message_creation_ai(self):
        """Test creating a ChatMessage with AIMessage."""
        chat_id = uuid4()
        message_id = uuid4()
        msg = AIMessage(content="Hello, how can I help?")
        now = datetime.datetime.now()

        chat_message = ChatMessage(
            chat_id=chat_id,
            message_id=message_id,
            brain_id=None,
            msg=msg,
            message_time=now,
            metadata={},
        )

        assert chat_message.brain_id is None
        assert isinstance(chat_message.msg, AIMessage)

    def test_chat_message_validation(self):
        """Test ChatMessage validation."""
        # Test with invalid UUID
        with pytest.raises(ValidationError):
            ChatMessage(
                chat_id="invalid-uuid",
                message_id=uuid4(),
                brain_id=None,
                msg=HumanMessage(content="test"),
                message_time=datetime.datetime.now(),
                metadata={},
            )


class TestKnowledgeStatus:
    """Test the KnowledgeStatus enum."""

    def test_knowledge_status_values(self):
        """Test that all expected status values exist."""
        expected_statuses = ["ERROR", "RESERVED", "PROCESSING", "PROCESSED", "UPLOADED"]

        for status in expected_statuses:
            assert hasattr(KnowledgeStatus, status)
            assert getattr(KnowledgeStatus, status) == status

    def test_knowledge_status_usage(self):
        """Test using KnowledgeStatus in comparisons."""
        assert KnowledgeStatus.PROCESSED == "PROCESSED"
        assert KnowledgeStatus.ERROR != KnowledgeStatus.PROCESSING


class TestSource:
    """Test the Source model."""

    def test_source_creation(self):
        """Test creating a Source instance."""
        source = Source(
            name="Document 1",
            source_url="https://example.com/doc1.pdf",
            type="pdf",
            original_file_name="doc1.pdf",
            citation="Page 5, Document 1",
        )

        assert source.name == "Document 1"
        assert source.source_url == "https://example.com/doc1.pdf"
        assert source.type == "pdf"
        assert source.original_file_name == "doc1.pdf"
        assert source.citation == "Page 5, Document 1"

    def test_source_validation(self):
        """Test Source validation."""
        with pytest.raises(ValidationError):
            Source()  # Missing required fields


class TestChatLLMMetadata:
    """Test the ChatLLMMetadata model."""

    def test_chat_llm_metadata_minimal(self):
        """Test creating ChatLLMMetadata with minimal data."""
        metadata = ChatLLMMetadata(name="gpt-4")

        assert metadata.name == "gpt-4"
        assert metadata.display_name is None
        assert metadata.description is None
        assert metadata.image_url is None
        assert metadata.brain_id is None
        assert metadata.brain_name is None

    def test_chat_llm_metadata_full(self):
        """Test creating ChatLLMMetadata with all fields."""
        metadata = ChatLLMMetadata(
            name="gpt-4",
            display_name="GPT-4",
            description="Advanced language model",
            image_url="https://example.com/gpt4.png",
            brain_id="brain-123",
            brain_name="Main Brain",
        )

        assert metadata.name == "gpt-4"
        assert metadata.display_name == "GPT-4"
        assert metadata.description == "Advanced language model"
        assert metadata.image_url == "https://example.com/gpt4.png"
        assert metadata.brain_id == "brain-123"
        assert metadata.brain_name == "Main Brain"


class TestRAGResponseMetadata:
    """Test the RAGResponseMetadata model."""

    def test_rag_response_metadata_defaults(self):
        """Test default values for RAGResponseMetadata."""
        metadata = RAGResponseMetadata()

        assert metadata.citations == []
        assert metadata.followup_questions == []
        assert metadata.sources == []
        assert metadata.metadata_model is None
        assert metadata.workflow_step is None

    def test_rag_response_metadata_with_data(self):
        """Test RAGResponseMetadata with data."""
        llm_metadata = ChatLLMMetadata(name="gpt-4")
        metadata = RAGResponseMetadata(
            citations=[1, 2],
            followup_questions=["What next?"],
            sources=["doc1.pdf"],
            metadata_model=llm_metadata,
            workflow_step="generate",
        )

        assert metadata.citations == [1, 2]
        assert metadata.followup_questions == ["What next?"]
        assert metadata.sources == ["doc1.pdf"]
        assert metadata.metadata_model == llm_metadata
        assert metadata.workflow_step == "generate"

    def test_rag_response_metadata_field_factories(self):
        """Test that default factories create separate instances."""
        metadata1 = RAGResponseMetadata()
        metadata2 = RAGResponseMetadata()

        # Modify one instance
        metadata1.citations.append(1)

        # Other instance should be unaffected
        assert metadata2.citations == []


class TestParsedRAGResponse:
    """Test the ParsedRAGResponse model."""

    def test_parsed_rag_response_minimal(self):
        """Test creating ParsedRAGResponse with minimal data."""
        response = ParsedRAGResponse(answer="This is the answer")

        assert response.answer == "This is the answer"
        assert response.metadata is None

    def test_parsed_rag_response_with_metadata(self):
        """Test creating ParsedRAGResponse with metadata."""
        metadata = RAGResponseMetadata(citations=[1, 2])
        response = ParsedRAGResponse(answer="This is the answer", metadata=metadata)

        assert response.answer == "This is the answer"
        assert response.metadata == metadata


class TestParsedRAGChunkResponse:
    """Test the ParsedRAGChunkResponse model."""

    def test_parsed_rag_chunk_response_creation(self):
        """Test creating ParsedRAGChunkResponse."""
        metadata = RAGResponseMetadata()
        chunk = ParsedRAGChunkResponse(
            answer="Partial answer", metadata=metadata, last_chunk=False
        )

        assert chunk.answer == "Partial answer"
        assert chunk.metadata == metadata
        assert chunk.last_chunk is False

    def test_parsed_rag_chunk_response_last_chunk_default(self):
        """Test default value for last_chunk."""
        metadata = RAGResponseMetadata()
        chunk = ParsedRAGChunkResponse(answer="Partial answer", metadata=metadata)

        assert chunk.last_chunk is False


class TestQuivrKnowledge:
    """Test the QuivrKnowledge model."""

    def test_quivr_knowledge_minimal(self):
        """Test creating QuivrKnowledge with minimal required fields."""
        knowledge_id = uuid4()
        knowledge = QuivrKnowledge(id=knowledge_id, file_name="test.txt")

        assert knowledge.id == knowledge_id
        assert knowledge.file_name == "test.txt"
        assert knowledge.brain_ids is None
        assert knowledge.url is None
        assert knowledge.extension == ".txt"
        assert knowledge.mime_type == "txt"
        assert knowledge.status == KnowledgeStatus.PROCESSING
        assert knowledge.source is None

    def test_quivr_knowledge_full(self):
        """Test creating QuivrKnowledge with all fields."""
        knowledge_id = uuid4()
        brain_id = uuid4()
        now = datetime.datetime.now()

        knowledge = QuivrKnowledge(
            id=knowledge_id,
            file_name="document.pdf",
            brain_ids=[brain_id],
            url="https://example.com/doc.pdf",
            extension=".pdf",
            mime_type="application/pdf",
            status=KnowledgeStatus.PROCESSED,
            source="upload",
            source_link="https://example.com/doc.pdf",
            file_size=1024,
            file_sha1="abc123",
            updated_at=now,
            created_at=now,
            metadata={"category": "research"},
        )

        assert knowledge.id == knowledge_id
        assert knowledge.file_name == "document.pdf"
        assert knowledge.brain_ids == [brain_id]
        assert knowledge.url == "https://example.com/doc.pdf"
        assert knowledge.extension == ".pdf"
        assert knowledge.mime_type == "application/pdf"
        assert knowledge.status == KnowledgeStatus.PROCESSED
        assert knowledge.source == "upload"
        assert knowledge.source_link == "https://example.com/doc.pdf"
        assert knowledge.file_size == 1024
        assert knowledge.file_sha1 == "abc123"
        assert knowledge.updated_at == now
        assert knowledge.created_at == now
        assert knowledge.metadata == {"category": "research"}

    def test_quivr_knowledge_validation(self):
        """Test QuivrKnowledge validation."""
        # Test with invalid UUID
        with pytest.raises(ValidationError):
            QuivrKnowledge(id="invalid-uuid", file_name="test.txt")

    def test_quivr_knowledge_status_enum(self):
        """Test that status field accepts KnowledgeStatus enum."""
        knowledge_id = uuid4()

        for status in KnowledgeStatus:
            knowledge = QuivrKnowledge(
                id=knowledge_id, file_name="test.txt", status=status
            )
            assert knowledge.status == status


class TestSearchResult:
    """Test the SearchResult model."""

    def test_search_result_creation(self):
        """Test creating a SearchResult instance."""
        document = Document(
            page_content="Sample content", metadata={"source": "test.pdf"}
        )

        result = SearchResult(chunk=document, distance=0.75)

        assert result.chunk == document
        assert result.distance == 0.75

    def test_search_result_validation(self):
        """Test SearchResult validation."""
        with pytest.raises(ValidationError):
            SearchResult()  # Missing required fields

        with pytest.raises(ValidationError):
            SearchResult(
                chunk="not a document",  # Wrong type
                distance=0.5,
            )


class TestTypedDictModels:
    """Test the TypedDict models."""

    def test_raw_rag_chunk_response_type(self):
        """Test RawRAGChunkResponse TypedDict structure."""
        # TypedDict doesn't enforce types at runtime, but we can test usage
        chunk_response: RawRAGChunkResponse = {
            "answer": {"content": "test"},
            "docs": {"documents": []},
        }

        assert "answer" in chunk_response
        assert "docs" in chunk_response

    def test_raw_rag_response_type(self):
        """Test RawRAGResponse TypedDict structure."""
        response: RawRAGResponse = {
            "answer": {"content": "test answer"},
            "docs": {"documents": []},
        }

        assert "answer" in response
        assert "docs" in response


class TestModelSerialization:
    """Test model serialization and deserialization."""

    def test_cited_answer_serialization(self):
        """Test cited_answer model serialization."""
        answer = cited_answer(
            answer="Test answer",
            citations=[1, 2],
            followup_questions=["Question 1", "Question 2"],
        )

        # Test to dict
        data = answer.model_dump()
        assert data["answer"] == "Test answer"
        assert data["citations"] == [1, 2]
        assert data["followup_questions"] == ["Question 1", "Question 2"]

        # Test from dict
        new_answer = cited_answer.model_validate(data)
        assert new_answer == answer

    def test_rag_response_metadata_serialization(self):
        """Test RAGResponseMetadata serialization."""
        metadata = RAGResponseMetadata(
            citations=[1, 2], followup_questions=["What next?"], sources=["doc1.pdf"]
        )

        data = metadata.model_dump()
        new_metadata = RAGResponseMetadata.model_validate(data)
        assert new_metadata == metadata

    def test_quivr_knowledge_serialization(self):
        """Test QuivrKnowledge serialization."""
        knowledge = QuivrKnowledge(
            id=uuid4(), file_name="test.txt", status=KnowledgeStatus.PROCESSED
        )

        data = knowledge.model_dump()
        new_knowledge = QuivrKnowledge.model_validate(data)
        assert new_knowledge == knowledge


class TestModelEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_string_fields(self):
        """Test models with empty string fields."""
        knowledge = QuivrKnowledge(
            id=uuid4(),
            file_name="",  # Empty filename
        )
        assert knowledge.file_name == ""

    def test_large_lists(self):
        """Test models with large lists."""
        large_citations = list(range(1000))
        large_questions = [f"Question {i}" for i in range(100)]

        answer = cited_answer(
            answer="Test", citations=large_citations, followup_questions=large_questions
        )

        assert len(answer.citations) == 1000
        assert len(answer.followup_questions) == 100

    def test_unicode_content(self):
        """Test models with unicode content."""
        answer = cited_answer(
            answer="Réponse avec des caractères spéciaux: 你好, 🌟",
            citations=[1],
            followup_questions=["Quelle est la question suivante? 🤔"],
        )

        assert "你好" in answer.answer
        assert "🤔" in answer.followup_questions[0]

    def test_nested_model_validation(self):
        """Test nested model validation."""
        llm_metadata = ChatLLMMetadata(name="test-model")

        # Valid nested model
        metadata = RAGResponseMetadata(metadata_model=llm_metadata)
        assert metadata.metadata_model.name == "test-model"

        # Test serialization with nested model
        data = metadata.model_dump()
        new_metadata = RAGResponseMetadata.model_validate(data)
        assert new_metadata.metadata_model.name == "test-model"
