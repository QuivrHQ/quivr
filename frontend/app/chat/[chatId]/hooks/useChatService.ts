/* eslint-disable max-lines */

import { useCallback } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useChatContext } from "@/lib/context/ChatProvider/hooks/useChatContext";
import { useAxios, useFetch } from "@/lib/hooks";

import { ChatEntity, ChatHistory, ChatQuestion } from "../types";

interface UseChatService {
  createChat: (name: { name: string }) => Promise<ChatEntity>;
  getChatHistory: (chatId: string | undefined) => Promise<ChatHistory[]>;
  addQuestion: (chatId: string, chatQuestion: ChatQuestion) => Promise<void>;
  addStreamQuestion: (
    chatId: string,
    chatQuestion: ChatQuestion
  ) => Promise<void>;
}

export const useChatService = (): UseChatService => {
  const { axiosInstance } = useAxios();
  const { fetchInstance } = useFetch();
  const { updateHistory, updateStreamingHistory } = useChatContext();
  const { currentBrain } = useBrainContext();
  const createChat = async ({
    name,
  }: {
    name: string;
  }): Promise<ChatEntity> => {
    const response = (await axiosInstance.post<ChatEntity>(`/chat`, { name }))
      .data;

    return response;
  };

  const getChatHistory = useCallback(
    async (chatId: string | undefined): Promise<ChatHistory[]> => {
      if (chatId === undefined) {
        return [];
      }
      const response = (
        await axiosInstance.get<ChatHistory[]>(`/chat/${chatId}/history`)
      ).data;

      return response;
    },
    [axiosInstance]
  );

  const addQuestion = async (
    chatId: string,
    chatQuestion: ChatQuestion
  ): Promise<void> => {
    if (currentBrain?.id === undefined) {
      throw new Error("No current brain");
    }

    const response = await axiosInstance.post<ChatHistory>(
      `/chat/${chatId}/question?brain_id=${currentBrain.id}`,
      chatQuestion
    );

    updateHistory(response.data);
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
          console.error("Error parsing data:", error);
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
      throw new Error("No current brain");
    }
    const headers = {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    };
    const body = JSON.stringify(chatQuestion);

    try {
      const response = await fetchInstance.post(
        `/chat/${chatId}/question/stream?brain_id=${currentBrain.id}`,
        body,
        headers
      );

      if (response.body === null) {
        throw new Error("Response body is null");
      }

      console.log("Received response. Starting to handle stream...");
      await handleStream(response.body.getReader());
    } catch (error) {
      console.error("Error calling the API:", error);
    }
  };

  return {
    createChat,
    getChatHistory,
    addQuestion,
    addStreamQuestion,
  };
};
