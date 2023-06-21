import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { useBrainConfig } from "@/lib/context/BrainConfigProvider/hooks/useBrainConfig";
import { useAxios, useToast } from "@/lib/hooks";

import { useChatContext } from "../context/ChatContext";
import { ChatHistory, ChatQuestion } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChat = () => {
  const params = useParams();
  const chatId = params?.chatId as string | undefined;
  const [generatingAnswer, setGeneratingAnswer] = useState(false);
  const { axiosInstance } = useAxios();
  const {
    config: { maxTokens, model, temperature },
  } = useBrainConfig();
  const { history, setHistory, addMessage } = useChatContext();
  const { publish } = useToast();

  useEffect(() => {
    const fetchHistory = async () => {
      if (chatId === undefined) {
        return;
      }
      const rep = await axiosInstance.get<ChatHistory[]>(
        `/chat/${chatId}/history`
      );

      setHistory(rep.data);
    };
    void fetchHistory();
  }, [chatId, axiosInstance, setHistory]);

  const addQuestion = async (question: string, callback?: () => void) => {
    const chatQuestion: ChatQuestion = {
      model,
      question,
      temperature,
      max_tokens: maxTokens,
    };

    if (chatId === undefined) {
      return;
    }
    try {
      setGeneratingAnswer(true);
      const rep = await axiosInstance.post<ChatHistory>(
        `/chat/${chatId}/question`,
        chatQuestion
      );
      addMessage(rep.data);
      callback?.();
    } catch (error) {
      console.error(error);
      publish({
        variant: "danger",
        text: "Error occurred while getting answer",
      });
    } finally {
      setGeneratingAnswer(false);
    }
  };

  return { history, addQuestion, generatingAnswer };
};
