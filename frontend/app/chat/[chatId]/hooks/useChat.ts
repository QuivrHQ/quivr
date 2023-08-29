/* eslint-disable max-lines */
import { AxiosError } from "axios";
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { getChatConfigFromLocalStorage } from "@/lib/api/chat/chat.local";
import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
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
  const router = useRouter();
  const { history } = useChatContext();
  const { currentBrain, currentPromptId, currentBrainId } = useBrainContext();
  const { publish } = useToast();
  const { createChat } = useChatApi();

  const { addStreamQuestion } = useQuestion();
  const { t } = useTranslation(["chat"]);

  const addQuestion = async (question: string, callback?: () => void) => {
    if (question === "") {
      publish({
        variant: "danger",
        text: t("ask"),
      });

      return;
    }

    try {
      setGeneratingAnswer(true);

      let currentChatId = chatId;

      let shouldUpdateUrl = false;

      //if chatId is not set, create a new chat. Chat name is from the first question
      if (currentChatId === undefined) {
        const chatName = question.split(" ").slice(0, 3).join(" ");
        const chat = await createChat(chatName);
        currentChatId = chat.chat_id;
        setChatId(currentChatId);
        shouldUpdateUrl = true;
        //TODO: update chat list here
      }

      void track("QUESTION_ASKED", {
        brainId: currentBrainId,
        promptId: currentPromptId,
      });

      const chatConfig = getChatConfigFromLocalStorage(currentChatId);

      const chatQuestion: ChatQuestion = {
        model: chatConfig?.model,
        question,
        temperature: chatConfig?.temperature,
        max_tokens: chatConfig?.maxTokens,
        brain_id: currentBrain?.id,
        prompt_id: currentPromptId ?? undefined,
      };

      await addStreamQuestion(currentChatId, chatQuestion);

      callback?.();

      if (shouldUpdateUrl) {
        router.replace(`/chat/${currentChatId}`);
      }
    } catch (error) {
      console.error({ error });

      if ((error as AxiosError).response?.status === 429) {
        publish({
          variant: "danger",
          text: t("limit_reached", { ns: "chat" }),
        });

        return;
      }

      publish({
        variant: "danger",
        text: t("error_occurred", { ns: "chat" }),
      });
    } finally {
      setGeneratingAnswer(false);
    }
  };

  return {
    history,
    addQuestion,
    generatingAnswer,
    chatId,
  };
};
