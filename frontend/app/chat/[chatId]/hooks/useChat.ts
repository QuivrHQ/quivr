/* eslint-disable max-lines */
import { AxiosError } from "axios";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useBrainConfig } from "@/lib/context/BrainConfigProvider/hooks/useBrainConfig";
import { useChatContext } from "@/lib/context/ChatProvider/hooks/useChatContext";
import { useToast } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/useEventTracking";

import { useQuestion } from "./useQuestion";
import { ChatQuestion } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChat = () => {
  const { track } = useEventTracking();
  const params = useParams();
  const [chatId, setChatId] = useState<string | undefined>(
    params?.chatId as string | undefined
  );
  const [generatingAnswer, setGeneratingAnswer] = useState(false);
  const {
    config: { maxTokens, model, temperature },
  } = useBrainConfig();
  const { history, setHistory } = useChatContext();
  const { publish } = useToast();
  const { createChat, getHistory } = useChatApi();

  const { addStreamQuestion, addQuestion: addQuestionToModel } = useQuestion();

  useEffect(() => {
    const fetchHistory = async () => {
      const currentChatId = chatId;
      if (currentChatId === undefined) {
        return;
      }

      const chatHistory = await getHistory(currentChatId);

      if (chatId === currentChatId && chatHistory.length > 0) {
        setHistory(chatHistory);
      }
    };
    void fetchHistory();
  }, [chatId, setHistory]);

  const addQuestion = async (question: string, callback?: () => void) => {
    const chatQuestion: ChatQuestion = {
      model,
      question,
      temperature,
      max_tokens: maxTokens,
    };

    try {
      setGeneratingAnswer(true);

      let currentChatId = chatId;

      //if chatId is not set, create a new chat. Chat name is from the first question
      if (currentChatId === undefined) {
        const chatName = question.split(" ").slice(0, 3).join(" ");
        const chat = await createChat(chatName);
        currentChatId = chat.chat_id;
        setChatId(currentChatId);
      }

      void track("QUESTION_ASKED");

      if (chatQuestion.model === "gpt-3.5-turbo") {
        await addStreamQuestion(currentChatId, chatQuestion);
      } else {
        await addQuestionToModel(currentChatId, chatQuestion);
      }

      callback?.();
    } catch (error) {
      console.error({ error });

      if ((error as AxiosError).response?.status === 429) {
        publish({
          variant: "danger",
          text: "You have reached the limit of requests, please try again later",
        });

        return;
      }

      publish({
        variant: "danger",
        text: "Error occurred while getting answer",
      });
    } finally {
      setGeneratingAnswer(false);
    }
  };

  return {
    history,
    addQuestion,
    generatingAnswer,
  };
};
