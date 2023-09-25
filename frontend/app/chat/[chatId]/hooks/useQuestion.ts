import { useTranslation } from "react-i18next";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useFetch, useToast } from "@/lib/hooks";

import { useHandleStream } from "./useHandleStream";
import { ChatQuestion } from "../types";

interface UseChatService {
  addStreamQuestion: (
    chatId: string,
    chatQuestion: ChatQuestion
  ) => Promise<void>;
}

export const useQuestion = (): UseChatService => {
  const { fetchInstance } = useFetch();
  const { currentBrain } = useBrainContext();

  const { t } = useTranslation(["chat"]);
  const { publish } = useToast();
  const { handleStream } = useHandleStream();

  const handleFetchError = async (response: Response) => {
    if (response.status === 429) {
      publish({
        variant: "danger",
        text: t("tooManyRequests", { ns: "chat" }),
      });

      return;
    }

    const errorMessage = (await response.json()) as { detail: string };
    publish({
      variant: "danger",
      text: errorMessage.detail,
    });

    return;
  };

  const addStreamQuestion = async (
    chatId: string,
    chatQuestion: ChatQuestion
  ): Promise<void> => {
    const headers = {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    };
    const body = JSON.stringify(chatQuestion);

    try {
      const response = await fetchInstance.post(
        `/chat/${chatId}/question/stream?brain_id=${currentBrain?.id ?? ""}`,
        body,
        headers
      );
      if (!response.ok) {
        void handleFetchError(response);

        return;
      }

      if (response.body === null) {
        throw new Error(t("resposeBodyNull", { ns: "chat" }));
      }

      await handleStream(response.body.getReader());
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
