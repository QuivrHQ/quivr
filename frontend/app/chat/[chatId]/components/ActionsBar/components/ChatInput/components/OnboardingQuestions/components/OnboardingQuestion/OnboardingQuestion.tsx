import { Fragment } from "react";

import { useChatInput } from "@/app/chat/[chatId]/components/ActionsBar/components/ChatInput/hooks/useChatInput";
import { useChat } from "@/app/chat/[chatId]/hooks/useChat";
import Button from "@/lib/components/ui/Button";
import { useOnboarding } from "@/lib/hooks/useOnboarding";

import { QuestionId } from "../../types";
// eslint-disable-next-line import/order
import { useOnboardingQuestion } from "./hooks/useOnboardingQuestion";

type OnboardingQuestionsProps = {
  questionId: QuestionId;
};

export const OnboardingQuestion = ({
  questionId,
}: OnboardingQuestionsProps): JSX.Element => {
  const { onboarding } = useOnboarding();
  const { question } = useOnboardingQuestion(questionId);
  const { setMessage } = useChatInput();

  const { addQuestion, generatingAnswer } = useChat();

  if (!onboarding[questionId]) {
    return <Fragment />;
  }

  const generateBoardingChat = () => {
    if (!generatingAnswer) {
      void addQuestion(question, () => setMessage(""));
    }
  };

  return (
    <Button
      className="sm:px-6 sm:py-3"
      variant={"secondary"}
      isLoading={generatingAnswer}
      onClick={() => void generateBoardingChat()}
    >
      {question}
    </Button>
  );
};
