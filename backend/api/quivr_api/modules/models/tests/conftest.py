from typing import Tuple

import pytest
import pytest_asyncio
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from quivr_api.modules.models.entity.model import Model
from quivr_api.modules.user.entity.user_identity import User

TestData = Tuple[Model, Model, User]


@pytest_asyncio.fixture(scope="function")
async def test_data(
    session: AsyncSession,
) -> TestData:
    # User data
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()

    model_1 = Model(
        name="this-is-a-fake-model", price=1, max_input=4000, max_output=2000
    )
    model_2 = Model(
        name="this-is-another-fake-model", price=5, max_input=8000, max_output=4000
    )

    session.add(model_1)
    session.add(model_2)

    await session.commit()
    await session.refresh(user_1)
    await session.refresh(model_1)
    await session.refresh(model_2)
    return model_1, model_2, user_1


@pytest.fixture
def sample_models():
    return [
        Model(name="gpt-3.5-turbo", price=1, max_input=4000, max_output=2000),
        Model(name="gpt-4", price=5, max_input=8000, max_output=4000),
    ]
