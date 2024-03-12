import { useContext } from "react";

import {
  OnboardingContext,
  OnboardingContextType,
} from "../Onboarding-provider";

export const useOnboardingContext = (): OnboardingContextType => {
  const context = useContext(OnboardingContext);
  if (context === undefined) {
    throw new Error("useMenuContext must be used within a MenuProvider");
  }

  return context;
};
