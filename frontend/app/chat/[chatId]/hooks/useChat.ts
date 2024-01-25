/* eslint-disable max-lines */
import { useQueryClient } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { CHATS_DATA_KEY } from "@/lib/api/chat/config";
import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useChatContext } from "@/lib/context";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { getChatNameFromQuestion } from "@/lib/helpers/getChatNameFromQuestion";
import { useToast } from "@/lib/hooks";
import { useOnboarding } from "@/lib/hooks/useOnboarding";
import { useOnboardingTracker } from "@/lib/hooks/useOnboardingTracker";
import { useEventTracking } from "@/services/analytics/june/useEventTracking";

import { useLocalStorageChatConfig } from "./useLocalStorageChatConfig";
import { useQuestion } from "./useQuestion";

import { ChatQuestion } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChat = () => {
  const { track } = useEventTracking();
  const queryClient = useQueryClient();

  const params = useParams();
  const [chatId, setChatId] = useState<string | undefined>(
    params?.chatId as string | undefined
  );
  const { isOnboarding } = useOnboarding();
  const { trackOnboardingEvent } = useOnboardingTracker();
  const [generatingAnswer, setGeneratingAnswer] = useState(false);
  const router = useRouter();
  const { messages } = useChatContext();
  const { currentBrain, currentPromptId, currentBrainId } = useBrainContext();
  const { publish } = useToast();
  const { createChat } = useChatApi();
  const {
    chatConfig: { model, maxTokens, temperature },
  } = useLocalStorageChatConfig();

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

      //if chatId is not set, create a new chat. Chat name is from the first question
      if (currentChatId === undefined) {
        const chat = await createChat(getChatNameFromQuestion(question));
        currentChatId = chat.chat_id;
        setChatId(currentChatId);
        router.push(`/chat/${currentChatId}`);
        void queryClient.invalidateQueries({
          queryKey: [CHATS_DATA_KEY],
        });
      }

      if (isOnboarding) {
        void trackOnboardingEvent("QUESTION_ASKED", {
          brainId: currentBrainId,
          promptId: currentPromptId,
        });
      } else {
        void track("QUESTION_ASKED", {
          brainId: currentBrainId,
          promptId: currentPromptId,
        });
      }

      const chatQuestion: ChatQuestion = {
        model, // eslint-disable-line @typescript-eslint/no-unsafe-assignment
        question,
        temperature: temperature,
        max_tokens: maxTokens,
        brain_id: currentBrain?.id,
        prompt_id: currentPromptId ?? undefined,
      };

      callback?.();
      await addStreamQuestion(currentChatId, chatQuestion);
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
    messages,
    addQuestion,
    generatingAnswer,
    chatId,
  };
};
