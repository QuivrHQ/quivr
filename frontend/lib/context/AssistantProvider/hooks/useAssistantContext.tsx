import { useContext } from "react";

import { AssistantContext, AssistantContextType } from "../Assistant-provider";

export const useAssistantContext = (): AssistantContextType => {
  const context = useContext(AssistantContext);
  if (context === undefined) {
    throw new Error(
      "useAssistantContext must be used within a OnboardingProvider"
    );
  }

  return context;
};
