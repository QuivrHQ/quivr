import { OnboardingProgress, OnboardingState } from "../../types";

const onboardingStepToState: Record<OnboardingProgress, OnboardingState[]> = {
  STEP_1: ["DOWNLOAD"],
  STEP_2: ["UPLOAD"],
};

type CheckIfShouldDisplayStepProps = {
  currentStep: OnboardingState;
  step: OnboardingProgress;
};

export const checkIfShouldDisplayStep = ({
  currentStep,
  step,
}: CheckIfShouldDisplayStepProps): boolean => {
  return onboardingStepToState[step].includes(currentStep);
};
