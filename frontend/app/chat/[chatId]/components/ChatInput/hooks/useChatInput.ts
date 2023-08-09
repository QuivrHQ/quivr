import { useState } from "react";

import { useChat } from "../../../hooks/useChat";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChatInput = () => {
  const [message, setMessage] = useState<string>("");
  const { addQuestion, generatingAnswer, chatId } = useChat();

  const submitQuestion = () => {
    if (message.length === 0) {
      return;
    }
    if (!generatingAnswer) {
      void addQuestion(message, () => setMessage(""));
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
