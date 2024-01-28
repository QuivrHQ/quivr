import uuid
from datetime import datetime
from unittest.mock import create_autospec

import pytest
from modules.brain.dto.inputs import CreateBrainProperties
from modules.brain.entity.brain_entity import BrainEntity, BrainType
from modules.brain.repository.interfaces.brains_interface import BrainsInterface


@pytest.fixture
def mock_brains_interface():
    return create_autospec(BrainsInterface)


def test_create_brain(mock_brains_interface):
    brain = CreateBrainProperties()
    mock_brains_interface.create_brain.return_value = BrainEntity(
        brain_id=uuid.uuid4(),  # generate a valid UUID
        name="test_name",
        last_update=datetime.now().isoformat(),  # convert datetime to string
        brain_type=BrainType.DOC,
    )
    result = mock_brains_interface.create_brain(brain)
    mock_brains_interface.create_brain.assert_called_once_with(brain)
    assert isinstance(result, BrainEntity)


def test_brain_entity_creation():
    brain_id = uuid.uuid4()
    name = "test_name"
    last_update = datetime.now().isoformat()
    brain_type = BrainType.DOC

    brain_entity = BrainEntity(
        brain_id=brain_id, name=name, last_update=last_update, brain_type=brain_type
    )

    assert brain_entity.brain_id == brain_id
    assert brain_entity.name == name
    assert brain_entity.last_update == last_update
    assert brain_entity.brain_type == brain_type


def test_brain_entity_id_property():
    brain_id = uuid.uuid4()
    name = "test_name"
    last_update = datetime.now().isoformat()
    brain_type = BrainType.DOC

    brain_entity = BrainEntity(
        brain_id=brain_id, name=name, last_update=last_update, brain_type=brain_type
    )

    assert brain_entity.id == brain_id


def test_brain_entity_dict_method():
    brain_id = uuid.uuid4()
    name = "test_name"
    last_update = datetime.now().isoformat()
    brain_type = BrainType.DOC

    brain_entity = BrainEntity(
        brain_id=brain_id, name=name, last_update=last_update, brain_type=brain_type
    )

    brain_dict = brain_entity.dict()
    assert brain_dict["id"] == brain_id
    assert brain_dict["name"] == name
    assert brain_dict["last_update"] == last_update
    assert brain_dict["brain_type"] == brain_type
