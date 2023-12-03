from pydantic import BaseModel


class OnboardingStates(BaseModel):
    """Response when getting onboarding"""

    onboarding_a: bool
    onboarding_b1: bool
    onboarding_b2: bool
    onboarding_b3: bool
