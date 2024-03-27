import { useContext } from "react";

import {
  OnboardingContext,
  OnboardingContextType,
} from "../Onboarding-provider";

export const useOnboardingContext = (): OnboardingContextType => {
  const context = useContext(OnboardingContext);
  if (context === undefined) {
    throw new Error(
      "useOnboardingContext must be used within a OnboardingProvider"
    );
  }

  return context;
};
