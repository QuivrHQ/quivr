import { OnboardingState } from "@/lib/context/OnboardingContext/types";

const requiredStateForDisplaying: Record<OnboardingState, OnboardingState[]> = {
  DOWNLOAD: ["DOWNLOAD", "UPLOAD", "UPLOADED"],
  UPLOAD: ["UPLOAD", "UPLOADED"],
  UPLOADED: ["UPLOADED"],
};

type CheckIfShouldDisplayStepProps = {
  currentStep: OnboardingState;
  step: OnboardingState;
};

export const checkIfShouldDisplayStep = ({
  currentStep,
  step,
}: CheckIfShouldDisplayStepProps): boolean => {
  return requiredStateForDisplaying[step].includes(currentStep);
};
