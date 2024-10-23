import { useCallback, useState } from "react";

import { useChat } from "@/app/chat/[chatId]/hooks/useChat";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChatInput = () => {
  const [message, setMessage] = useState<string>("");
  const { addQuestion, generatingAnswer, chatId } = useChat();

  const submitQuestion = useCallback(
    (question?: string, redirect = true) => {
      console.log({ question });

      const finalMessage = question ?? message;
      if (!generatingAnswer) {
        void addQuestion(finalMessage, () => setMessage(""), redirect);
      }
    },
    [addQuestion, generatingAnswer, message]
  );

  return {
    message,
    setMessage,
    submitQuestion,
    generatingAnswer,
    chatId,
  };
};
