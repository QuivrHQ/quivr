import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { ChatMessage } from "@/app/chat/[chatId]/types";
import { useChatContext } from "@/lib/context";
import { useOnboarding } from "@/lib/hooks/useOnboarding";
import { useOnboardingTracker } from "@/lib/hooks/useOnboardingTracker";
import { useStreamText } from "@/lib/hooks/useStreamText";

import { QuestionId } from "../../../types";
import { questionIdToTradPath } from "../utils";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useOnboardingQuestion = (questionId: QuestionId) => {
  const { updateOnboarding } = useOnboarding();
  const { t } = useTranslation("chat");
  const { trackOnboardingEvent } = useOnboardingTracker();
  const [isAnswerRequested, setIsAnswerRequested] = useState(false);

  const onboardingStep = questionIdToTradPath[questionId];
  const question = t(`onboarding.${onboardingStep}`);
  const { updateStreamingHistory } = useChatContext();

  const { lastStream } = useStreamText({
    text: t(`onboarding.answer.${onboardingStep}`),
    enabled: isAnswerRequested,
  });

  useEffect(() => {
    if (isAnswerRequested) {
      const chatMessage: ChatMessage = {
        chat_id: questionId,
        message_id: questionId,
        user_message: question,
        assistant: lastStream,
        message_time: Date.now().toLocaleString(),
        brain_name: "Quivr",
      };
      void updateStreamingHistory(chatMessage);
    }
  }, [isAnswerRequested, question, questionId, lastStream]);

  const handleSuggestionClick = async () => {
    trackOnboardingEvent(onboardingStep);
    setIsAnswerRequested(true);
    await updateOnboarding({ [questionId]: false });
  };

  return {
    handleSuggestionClick,
    question,
  };
};
