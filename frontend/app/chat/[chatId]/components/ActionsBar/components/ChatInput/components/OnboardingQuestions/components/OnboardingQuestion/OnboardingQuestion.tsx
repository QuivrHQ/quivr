import { Fragment } from "react";
import { useTranslation } from "react-i18next";

import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { useOnboardingQuestion } from "./hooks/useOnboardingQuestion";
import { questionIdToTradPath } from "./utils";
import { QuestionId } from "../../types";

type OnboardingQuestionsProps = {
  questionId: QuestionId;
};

export const OnboardingQuestion = ({
  questionId,
}: OnboardingQuestionsProps): JSX.Element => {
  const { onboarding } = useOnboarding();
  const { t } = useTranslation("chat");
  const { handleSuggestionClick } = useOnboardingQuestion(questionId);

  if (!onboarding[questionId]) {
    return <Fragment />;
  }

  const onboardingStep = questionIdToTradPath[questionId];

  return (
    <div
      onClick={() => void handleSuggestionClick()}
      className="cursor-pointer shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow bg-yellow-100 px-3 py-1 rounded-xl border-black/10 dark:border-white/25"
    >
      {t(`onboarding.${onboardingStep}`)}
    </div>
  );
};
