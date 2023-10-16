import { UUID } from "crypto";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { ChatMessage } from "@/app/chat/[chatId]/types";
import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useChatContext } from "@/lib/context";
import { getChatNameFromQuestion } from "@/lib/helpers/getChatNameFromQuestion";
import { useOnboarding } from "@/lib/hooks/useOnboarding";
import { useOnboardingTracker } from "@/lib/hooks/useOnboardingTracker";
import { useStreamText } from "@/lib/hooks/useStreamText";

import { QuestionId } from "../../../types";
import { questionIdToTradPath } from "../utils";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useOnboardingQuestion = (questionId: QuestionId) => {
  const router = useRouter();
  const params = useParams();
  const { updateOnboarding } = useOnboarding();
  const { t } = useTranslation("chat");
  const { createChat } = useChatApi();
  const { trackOnboardingEvent } = useOnboardingTracker();
  const [isAnswerRequested, setIsAnswerRequested] = useState(false);

  const [chatId, setChatId] = useState(params?.chatId as UUID | undefined);

  const onboardingStep = questionIdToTradPath[questionId];
  const question = t(`onboarding.${onboardingStep}`);
  const answer = t(`onboarding.answer.${onboardingStep}`);
  const { updateStreamingHistory } = useChatContext();
  const { addQuestionAndAnswer } = useChatApi();
  const { lastStream, isDone } = useStreamText({
    text: answer,
    enabled: isAnswerRequested && chatId !== undefined,
  });

  const addQuestionAndAnswerToChat = async () => {
    if (chatId === undefined) {
      return;
    }

    await addQuestionAndAnswer(chatId, {
      question: question,
      answer: answer,
    });
    const shouldUpdateUrl = chatId !== params?.chatId;
    if (shouldUpdateUrl) {
      router.replace(`/chat/${chatId}`);
    }
  };

  useEffect(() => {
    if (!isDone) {
      return;
    }
    void addQuestionAndAnswerToChat();
  }, [isDone]);

  useEffect(() => {
    if (chatId === undefined) {
      return;
    }

    if (isAnswerRequested) {
      const chatMessage: ChatMessage = {
        chat_id: chatId,
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
    if (chatId === undefined) {
      const newChat = await createChat(getChatNameFromQuestion(question));
      setChatId(newChat.chat_id);
    }
    trackOnboardingEvent(onboardingStep);
    setIsAnswerRequested(true);

    await updateOnboarding({ [questionId]: false });
  };

  return {
    handleSuggestionClick,
    question,
  };
};
