import { useContext } from "react";

import { OnboardingContext } from "../context/OnboardingContext/knowledgeToFeed-provider";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useOnboardingContext = () => {
  const context = useContext(OnboardingContext);
  if (!context) {
    throw new Error(
      "useOnboardingContext must be used within a OnboardingContextProvider"
    );
  }

  return context;
};
