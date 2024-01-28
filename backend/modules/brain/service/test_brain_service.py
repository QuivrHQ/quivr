from unittest.mock import Mock
from uuid import UUID

from modules.brain.entity.brain_entity import BrainEntity
from modules.brain.service.brain_service import BrainService


def test_find_brain_from_question_with_history_and_brain_id():
    brain_service = BrainService()
    user = Mock()
    user.id = 1
    chat_id = UUID("12345678123456781234567812345678")
    question = "What is the meaning of life?"
    brain_id = UUID("87654321876543218765432187654321")
    history = [
        {
            "user_message": "What is AI?",
            "brain_id": UUID("87654321876543218765432187654321"),
        }
    ]
    vector_store = Mock()
    vector_store.find_brain_closest_query.return_value = []

    brain_entity_mock = Mock(spec=BrainEntity)  # Create a mock BrainEntity
    brain_service.get_brain_by_id = Mock(
        return_value=brain_entity_mock
    )  # Mock the get_brain_by_id method

    brain_to_use, metadata = brain_service.find_brain_from_question(
        brain_id, question, user, chat_id, history, vector_store
    )

    assert isinstance(brain_to_use, BrainEntity)
    assert "close_brains" in metadata
