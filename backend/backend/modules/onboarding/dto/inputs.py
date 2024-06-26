from typing import Optional

from pydantic import ConfigDict, BaseModel


class OnboardingUpdatableProperties(BaseModel):

    """Properties that can be received on onboarding update"""

    onboarding_a: Optional[bool] = None
    onboarding_b1: Optional[bool] = None
    onboarding_b2: Optional[bool] = None
    onboarding_b3: Optional[bool] = None
    model_config = ConfigDict(extra="forbid")
