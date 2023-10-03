import { OnboardingState } from "../../types";

const onboardingStepToState: Record<OnboardingState, OnboardingState[]> = {
  DOWNLOAD: ["DOWNLOAD", "UPLOAD"],
  UPLOAD: ["UPLOAD"],
};

type CheckIfShouldDisplayStepProps = {
  currentStep: OnboardingState;
  step: OnboardingState;
};

export const checkIfShouldDisplayStep = ({
  currentStep,
  step,
}: CheckIfShouldDisplayStepProps): boolean => {
  return onboardingStepToState[step].includes(currentStep);
};
