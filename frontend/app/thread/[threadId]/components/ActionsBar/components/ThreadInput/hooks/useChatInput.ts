import { useCallback, useState } from "react";

import { useThread } from "@/app/thread/[threadId]/hooks/useThread";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useThreadInput = () => {
  const [message, setMessage] = useState<string>("");
  const { addQuestion, generatingAnswer, threadId } = useThread();

  const submitQuestion = useCallback(() => {
    if (!generatingAnswer) {
      void addQuestion(message, () => setMessage(""));
    }
  }, [addQuestion, generatingAnswer, message]);

  return {
    message,
    setMessage,
    submitQuestion,
    generatingAnswer,
    threadId,
  };
};
