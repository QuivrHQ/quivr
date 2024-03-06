/* eslint-disable max-lines */
import { useQueryClient } from "@tanstack/react-query";
import { AxiosError } from "axios";
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { CHATS_DATA_KEY } from "@/lib/api/thread/config";
import { useThreadApi } from "@/lib/api/thread/useThreadApi";
import { useThreadContext } from "@/lib/context";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useSearchModalContext } from "@/lib/context/SearchModalProvider/hooks/useSearchModalContext";
import { getThreadNameFromQuestion } from "@/lib/helpers/getChatNameFromQuestion";
import { useToast } from "@/lib/hooks";
import { useOnboarding } from "@/lib/hooks/useOnboarding";
import { useOnboardingTracker } from "@/lib/hooks/useOnboardingTracker";
import { useEventTracking } from "@/services/analytics/june/useEventTracking";

import { useLocalStorageThreadConfig } from "./useLocalStorageChatConfig";
import { useQuestion } from "./useQuestion";

import { ThreadQuestion } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useThread = () => {
  const { track } = useEventTracking();
  const queryClient = useQueryClient();

  const params = useParams();
  const [threadId, setThreadId] = useState<string | undefined>(
    params?.threadId as string | undefined
  );
  const { isOnboarding } = useOnboarding();
  const { trackOnboardingEvent } = useOnboardingTracker();
  const [generatingAnswer, setGeneratingAnswer] = useState(false);
  const router = useRouter();
  const { messages } = useThreadContext();
  const { currentBrain, currentPromptId, currentBrainId } = useBrainContext();
  const { publish } = useToast();
  const { createThread } = useThreadApi();
  const {
    threadConfig: { model, maxTokens, temperature },
  } = useLocalStorageThreadConfig();
  const { isVisible } = useSearchModalContext();

  const { addStreamQuestion } = useQuestion();
  const { t } = useTranslation(["thread"]);

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

      let currentThreadId = threadId;

      //if threadId is not set, create a new thread. Thread name is from the first question
      if (currentThreadId === undefined || isVisible) {
        const thread = await createThread(getThreadNameFromQuestion(question));
        currentThreadId = thread.thread_id;
        setThreadId(currentThreadId);
        router.push(`/thread/${currentThreadId}`);
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

      const threadQuestion: ThreadQuestion = {
        model, // eslint-disable-line @typescript-eslint/no-unsafe-assignment
        question,
        temperature: temperature,
        max_tokens: maxTokens,
        brain_id: currentBrain?.id,
        prompt_id: currentPromptId ?? undefined,
      };

      callback?.();
      await addStreamQuestion(currentThreadId, threadQuestion);
    } catch (error) {
      console.error({ error });

      if ((error as AxiosError).response?.status === 429) {
        publish({
          variant: "danger",
          text: t("limit_reached", { ns: "thread" }),
        });

        return;
      }

      publish({
        variant: "danger",
        text: t("error_occurred", { ns: "thread" }),
      });
    } finally {
      setGeneratingAnswer(false);
    }
  };

  return {
    messages,
    addQuestion,
    generatingAnswer,
    threadId,
  };
};
