import { useTranslation } from "react-i18next";

import { OnboardingQuestion } from "./components";

export const OnboardingQuestions = (): JSX.Element => {
  const { t } = useTranslation(["chat"]);

  const onboardingQuestions = [
    t("onboarding.how_to_use_quivr"),
    t("onboarding.what_is_quivr"),
    t("onboarding.what_is_brain"),
  ];

  return (
    <div className="flex flex-row flex-1 gap-4 mb-4">
      {onboardingQuestions.map((question) => (
        <OnboardingQuestion key={question} question={question} />
      ))}
    </div>
  );
};
