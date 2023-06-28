/* eslint-disable max-lines */
import { AxiosError } from "axios";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { useBrainConfig } from "@/lib/context/BrainConfigProvider/hooks/useBrainConfig";
import { generateUUID } from "@/lib/helpers/uuid";
import { useToast } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/useEventTracking";

import { useChatService } from "./useChatService";
import { useChatContext } from "../context/ChatContext";
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
  const { history, setHistory, addToHistory } = useChatContext();
  const { publish } = useToast();

  const {
    createChat,
    getChatHistory,
    addStreamQuestion,
    addQuestion: addQuestionToModel,
  } = useChatService();

  useEffect(() => {
    const fetchHistory = async () => {
      const currentChatId = chatId;
      const chatHistory = await getChatHistory(currentChatId);

      if (chatId === currentChatId && chatHistory.length > 0) {
        setHistory(chatHistory);
      }
    };
    void fetchHistory();
  }, [chatId, getChatHistory, setHistory]);

  const generateNewChatIdFromName = async (
    chatName: string
  ): Promise<string> => {
    const chat = await createChat({ name: chatName });

    return chat.chat_id;
  };

  const addQuestion = async (question: string, callback?: () => void) => {
    const chatQuestion: ChatQuestion = {
      model,
      question,
      temperature,
      max_tokens: maxTokens,
    };

    try {
      void track("QUESTION_ASKED");
      setGeneratingAnswer(true);
      const currentChatId =
        chatId ??
        // if chatId is undefined, we need to create a new chat on fly
        (await generateNewChatIdFromName(
          question.split(" ").slice(0, 3).join(" ")
        ));

      setChatId(currentChatId);

      //create a temp message_id, this is overwritten by the response from the backend
      const chatHistoryItem = {
        assistant: "",
        chat_id: currentChatId,
        message_id: generateUUID(),
        message_time: Date.now().toString(),
        user_message: chatQuestion.question ?? "",
      };

      addToHistory(chatHistoryItem);

      if (chatQuestion.model === "gpt-3.5-turbo") {
        await addStreamQuestion(currentChatId, chatQuestion, chatHistoryItem);
      } else {
        await addQuestionToModel(currentChatId, chatQuestion, chatHistoryItem);
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
