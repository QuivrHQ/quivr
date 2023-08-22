import axios from "axios";
import { useTranslation } from "react-i18next";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useChatContext } from "@/lib/context/ChatProvider/hooks/useChatContext";
import { useFetch, useToast } from "@/lib/hooks";

import { ChatHistory, ChatQuestion } from "../types";

interface UseChatService {
  addStreamQuestion: (
    chatId: string,
    chatQuestion: ChatQuestion
  ) => Promise<void>;
}

export const useQuestion = (): UseChatService => {
  const { fetchInstance } = useFetch();
  const { updateStreamingHistory } = useChatContext();
  const { currentBrain } = useBrainContext();

  const { t } = useTranslation(["chat"]);
  const { publish } = useToast();

  const handleStream = async (
    reader: ReadableStreamDefaultReader<Uint8Array>
  ): Promise<void> => {
    const decoder = new TextDecoder("utf-8");

    const handleStreamRecursively = async () => {
      const { done, value } = await reader.read();

      if (done) {
        return;
      }

      const dataStrings = decoder
        .decode(value)
        .trim()
        .split("data: ")
        .filter(Boolean);

      dataStrings.forEach((data) => {
        try {
          const parsedData = JSON.parse(data) as ChatHistory;
          updateStreamingHistory(parsedData);
        } catch (error) {
          console.error(t("errorParsingData", { ns: "chat" }), error);
        }
      });

      await handleStreamRecursively();
    };

    await handleStreamRecursively();
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
    console.log("Calling API...");
    try {
      const response = await fetchInstance.post(
        `/chat/${chatId}/question/stream?brain_id=${currentBrain?.id ?? ""}`,
        body,
        headers
      );

      if (response.body === null) {
        throw new Error(t("resposeBodyNull", { ns: "chat" }));
      }

      console.log(t("receivedResponse"), response);
      await handleStream(response.body.getReader());
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.status === 429) {
        publish({
          variant: "danger",
          text: t("tooManyRequests", { ns: "chat" }),
        });
      }

      console.error(t("errorCallingAPI", { ns: "chat" }), error);
    }
  };

  return {
    addStreamQuestion,
  };
};
