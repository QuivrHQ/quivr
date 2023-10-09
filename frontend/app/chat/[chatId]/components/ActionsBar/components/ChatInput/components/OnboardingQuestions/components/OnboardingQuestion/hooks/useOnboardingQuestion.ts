import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { QuestionId } from "../../../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useOnboardingQuestion = (questionId: QuestionId) => {
  const { updateOnboarding } = useOnboarding();

  const handleSuggestionClick = async () => {
    await updateOnboarding({ [questionId]: false });
  };

  return {
    handleSuggestionClick,
  };
};
