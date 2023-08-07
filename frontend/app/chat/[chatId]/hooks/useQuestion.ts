/* eslint-disable max-lines */

import { useTranslation } from "react-i18next";

import { useChatApi } from "@/lib/api/chat/useChatApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useChatContext } from "@/lib/context/ChatProvider/hooks/useChatContext";
import { useFetch } from "@/lib/hooks";

import { ChatHistory, ChatQuestion } from "../types";

interface UseChatService {
  addQuestion: (chatId: string, chatQuestion: ChatQuestion) => Promise<void>;
  addStreamQuestion: (
    chatId: string,
    chatQuestion: ChatQuestion
  ) => Promise<void>;
}

export const useQuestion = (): UseChatService => {
  const { fetchInstance } = useFetch();
  const { updateHistory, updateStreamingHistory } = useChatContext();
  const { currentBrain } = useBrainContext();
  const { addQuestion } = useChatApi();
  const { t } = useTranslation(['chat']);

  const addQuestionHandler = async (
    chatId: string,
    chatQuestion: ChatQuestion
  ): Promise<void> => {
    if (currentBrain?.id === undefined) {
      throw new Error(t("noCurrentBrain",{ns:'chat'}));
    }

    const response = await addQuestion({
      chatId,
      brainId: currentBrain.id,
      chatQuestion,
    });

    updateHistory(response);
  };

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
          console.error(t("errorParsingData",{ns:'chat'}), error);
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
    if (currentBrain?.id === undefined) {
      throw new Error(t("noCurrentBrain",{ns:'chat'}));
    }
    const headers = {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    };
    const body = JSON.stringify(chatQuestion);
    console.log("Calling API...");
    try {
      const response = await fetchInstance.post(
        `/chat/${chatId}/question/stream?brain_id=${currentBrain.id}`,
        body,
        headers
      );

      if (response.body === null) {
        throw new Error(t("resposeBodyNull",{ns:'chat'}));
      }

      console.log(t("receivedResponse"), response);
      await handleStream(response.body.getReader());
    } catch (error) {
      console.error(t("errorCallingAPI",{ns:"chat"}), error);
    }
  };

  return {
    addQuestion: addQuestionHandler,
    addStreamQuestion,
  };
};
