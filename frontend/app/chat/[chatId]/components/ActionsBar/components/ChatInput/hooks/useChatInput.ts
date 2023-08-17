import { useState } from "react";

import { useChat } from "@/app/chat/[chatId]/hooks/useChat";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChatInput = () => {
  const [message, setMessage] = useState<string>("");
  const { addQuestion, generatingAnswer, chatId } = useChat();

  const submitQuestion = (currentMessage?: string) => {
    const messageToSubmit = currentMessage ?? message;
    if (messageToSubmit.length === 0) {
      return;
    }
    if (!generatingAnswer) {
      void addQuestion(messageToSubmit, () => setMessage(""));
    }
  };

  return {
    message,
    setMessage,
    submitQuestion,
    generatingAnswer,
    chatId,
  };
};
