from typing import Optional

from pydantic import BaseModel


class OnboardingUpdatableProperties(BaseModel):

    """Properties that can be received on onboarding update"""

    onboarding_a: Optional[bool]
    onboarding_b1: Optional[bool]
    onboarding_b2: Optional[bool]
    onboarding_b3: Optional[bool]

    class Config:
        extra = "forbid"
