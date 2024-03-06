import { useTranslation } from "react-i18next";

import { useThreadContext } from "@/lib/context";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useFetch, useToast } from "@/lib/hooks";

import { useHandleStream } from "./useHandleStream";

import { ThreadQuestion } from "../types";
import { generatePlaceHolderMessage } from "../utils/generatePlaceHolderMessage";

interface UseThreadService {
  addStreamQuestion: (
    threadId: string,
    threadQuestion: ThreadQuestion
  ) => Promise<void>;
}

export const useQuestion = (): UseThreadService => {
  const { fetchInstance } = useFetch();
  const { currentBrain } = useBrainContext();

  const { t } = useTranslation(["thread"]);
  const { publish } = useToast();
  const { handleStream } = useHandleStream();
  const { removeMessage, updateStreamingHistory } = useThreadContext();

  const handleFetchError = async (response: Response) => {
    if (response.status === 429) {
      publish({
        variant: "danger",
        text: t("tooManyRequests", { ns: "thread" }),
      });

      return;
    }

    const errorMessage = (await response.json()) as { detail: string };
    publish({
      variant: "danger",
      text: errorMessage.detail,
    });
  };

  const addStreamQuestion = async (
    threadId: string,
    threadQuestion: ThreadQuestion
  ): Promise<void> => {
    const headers = {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    };

    const placeHolderMessage = generatePlaceHolderMessage({
      user_message: threadQuestion.question ?? "",
      thread_id: threadId,
    });
    updateStreamingHistory(placeHolderMessage);

    const body = JSON.stringify(threadQuestion);

    try {
      let url = `/thread/${threadId}/question/stream`;
      if (currentBrain?.id) {
        url += `?brain_id=${currentBrain.id}`;
      }
      const response = await fetchInstance.post(url, body, headers);
      if (!response.ok) {
        void handleFetchError(response);

        return;
      }

      if (response.body === null) {
        throw new Error(t("resposeBodyNull", { ns: "thread" }));
      }

      await handleStream(response.body.getReader(), () =>
        removeMessage(placeHolderMessage.message_id)
      );
    } catch (error) {
      publish({
        variant: "danger",
        text: String(error),
      });
    }
  };

  return {
    addStreamQuestion,
  };
};
