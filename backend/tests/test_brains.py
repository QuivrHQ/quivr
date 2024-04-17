import pytest
from modules.brain.dto.inputs import BrainIntegrationSettings, CreateBrainProperties
from modules.brain.entity.brain_entity import BrainEntity, BrainType
from modules.brain.service.brain_service import BrainService
from pydantic import ValidationError


@pytest.fixture
def brain_service():
    # Setup for brain service, if any
    service = BrainService()
    yield service
    # No teardown here, it will be handled in the test function


@pytest.fixture
def user_id():
    return "39418e3b-0258-4452-af60-7acfcc1263ff"


@pytest.fixture
def integration_id():
    return "b37a2275-61b3-460b-b4ab-94dfdf3642fb"


def test_create_brain_with_user_id(brain_service, user_id, integration_id):
    brain_id = None  # Initialize brain_id to None
    try:
        # Arrange
        brain_data = CreateBrainProperties(
            name="Innovative Brain",
            description="A brain representing innovative ideas",
            # Add other necessary fields and values
            brain_type="integration",
            integration=BrainIntegrationSettings(
                integration_id=integration_id,
                settings={},
            ),
        )

        # Act
        created_brain = brain_service.create_brain(user_id, brain_data)

        # Store the brain_id for teardown
        brain_id = created_brain.brain_id

        # Assert
        assert isinstance(created_brain, BrainEntity)
        assert created_brain.name == brain_data.name
        assert created_brain.description == brain_data.description
    finally:
        # Teardown step: delete the brain if it was created
        if brain_id:
            brain_service.delete_brain(brain_id)


def test_create_brain_with_invalid_user_id(brain_service):
    invalid_user_id = "invalid-uuid"
    brain_data = CreateBrainProperties(
        name="Brain with Invalid User ID",
        description="Should fail due to invalid user ID",
        brain_type="integration",
        integration=BrainIntegrationSettings(
            integration_id="valid-integration-id",
            settings={},
        ),
    )

    with pytest.raises(Exception):
        brain_service.create_brain(invalid_user_id, brain_data)


# Generate a test that checks CreateBrainProperties with invalid data
def test_create_brain_with_invalid_brain_type(brain_service):

    with pytest.raises(ValidationError):
        invalid_brain_data = CreateBrainProperties(
            name="Invalid Brain",
            description="Should fail due to invalid data",
            brain_type="invalid-brain-type",
            integration=BrainIntegrationSettings(
                integration_id="valid-integration-id",
                settings={},
            ),
        )


# Test for valid brain type 'integration'
def test_create_brain_with_valid_brain_type_integration(
    brain_service, user_id, integration_id
):
    brain_id = None
    try:
        valid_brain_data = CreateBrainProperties(
            name="Valid Integration Brain",
            description="Should succeed with valid integration brain type",
            brain_type="integration",
            integration=BrainIntegrationSettings(
                integration_id=integration_id,
                settings={},
            ),
        )

        created_brain = brain_service.create_brain(user_id, valid_brain_data)

        brain_id = created_brain.brain_id
        # Assert
        assert created_brain.brain_type == BrainType.INTEGRATION
    finally:
        # Teardown step: delete the brain if it was created
        if brain_id:
            brain_service.delete_brain(brain_id)


# Test for valid brain type 'doc'
def test_create_brain_with_valid_brain_type_doc(brain_service, user_id):
    brain_id = None
    try:
        valid_brain_data = CreateBrainProperties(
            name="Valid Doc Brain",
            description="Should succeed with valid doc brain type",
            brain_type="doc",
        )
        created_brain = brain_service.create_brain(user_id, valid_brain_data)
        assert created_brain.brain_type == BrainType.DOC
    finally:
        # Teardown step: delete the brain if it was created
        if brain_id:
            brain_service.delete_brain(brain_id)
