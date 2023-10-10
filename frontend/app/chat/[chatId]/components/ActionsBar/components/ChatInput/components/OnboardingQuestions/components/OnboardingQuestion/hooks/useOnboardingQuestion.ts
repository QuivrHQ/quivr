import { useTranslation } from "react-i18next";

import { useChat } from "@/app/chat/[chatId]/hooks/useChat";
import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { QuestionId } from "../../../types";
import { questionIdToTradPath } from "../utils";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useOnboardingQuestion = (questionId: QuestionId) => {
  const { updateOnboarding } = useOnboarding();
  const { t } = useTranslation("chat");

  const onboardingStep = questionIdToTradPath[questionId];

  const question = t(`onboarding.${onboardingStep}`);

  const { addQuestion } = useChat();

  const handleSuggestionClick = async () => {
    await Promise.all([
      addQuestion(question),
      updateOnboarding({ [questionId]: false }),
    ]);
  };

  return {
    handleSuggestionClick,
    question,
  };
};
