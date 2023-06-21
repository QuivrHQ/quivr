import { AxiosError } from "axios";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { useBrainConfig } from "@/lib/context/BrainConfigProvider/hooks/useBrainConfig";
import { useToast } from "@/lib/hooks";

import { useChatService } from "./useChatService";
import { useChatContext } from "../context/ChatContext";
import { ChatQuestion } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChat = () => {
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
    addQuestion: addQuestionToChat,
  } = useChatService();

  useEffect(() => {
    const fetchHistory = async () => {
      const chatHistory = await getChatHistory(chatId);
      setHistory(chatHistory);
    };
    void fetchHistory();
  }, [chatId]);

  const generateNewChatIdFromName = async (
    chatName: string
  ): Promise<string> => {
    const rep = await createChat({ name: chatName });
    setChatId(rep.data.chat_id);

    return rep.data.chat_id;
  };

  const addQuestion = async (question: string, callback?: () => void) => {
    const chatQuestion: ChatQuestion = {
      model,
      question,
      temperature,
      max_tokens: maxTokens,
    };

    try {
      setGeneratingAnswer(true);
      const currentChatId =
        chatId ??
        // if chatId is undefined, we need to create a new chat on fly
        (await generateNewChatIdFromName(
          question.split(" ").slice(0, 3).join(" ")
        ));
      const answer = await addQuestionToChat(currentChatId, chatQuestion);
      addToHistory(answer);
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

  return { history, addQuestion, generatingAnswer };
};
