import { OnboardingQuestion } from "./components";
import { QuestionId } from "./types";

export const OnboardingQuestions = (): JSX.Element => {
  const onboardingQuestions: QuestionId[] = [
    "onboarding_b1",
    "onboarding_b2",
    "onboarding_b3",
  ];

  return (
    <div className="flex flex-row flex-1 gap-4 mb-4">
      {onboardingQuestions.map((question) => (
        <OnboardingQuestion key={question} questionId={question} />
      ))}
    </div>
  );
};
