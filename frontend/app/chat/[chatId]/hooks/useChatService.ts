/* eslint-disable max-lines */

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useCallback } from "react";

import { useAxios } from "@/lib/hooks";
import { useFetch } from "@/lib/hooks/useFetch";

import { useChatContext } from "../context/ChatContext";
import { ChatEntity, ChatHistory, ChatQuestion } from "../types";

interface UseChatService {
  createChat: (name: { name: string }) => Promise<ChatEntity>;
  getChatHistory: (chatId: string | undefined) => Promise<ChatHistory[]>;
  addQuestion: (
    chatId: string,
    chatQuestion: ChatQuestion,
    chatHistory: ChatHistory
  ) => Promise<void>;
  addStreamQuestion: (
    chatId: string,
    chatQuestion: ChatQuestion,
    chatHistory: ChatHistory
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
    chatQuestion: ChatQuestion,
    chatHistory: ChatHistory
  ): Promise<void> => {
    if (currentBrain?.id === undefined) {
      throw new Error("No current brain");
    }

    const response = await axiosInstance.post<ChatHistory>(
      `/chat/${chatId}/question?brain_id=${currentBrain.id}`,
      chatQuestion
    );

    updateHistory(chatHistory.message_id, response.data);
  };

  const handleStream = async (
    reader: ReadableStreamDefaultReader,
    message_id: string
  ): Promise<void> => {
    const decoder = new TextDecoder("utf-8");
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      console.log("Reader status:", { done, value });

      if (done || value === undefined) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });
      const payloads = buffer.split("\n\n");
      buffer = payloads.pop() as string;

      payloads
        .filter((payload) => payload.startsWith("data:"))
        .map((dataPayload) =>
          dataPayload.replace("data: ", "").replace("\n\n", "")
        )
        .forEach((data: string) => {
          console.log("Received data:", data);
          updateStreamingHistory(message_id, data);
        });
    }
  };

  const addStreamQuestion = async (
    chatId: string,
    chatQuestion: ChatQuestion,
    chatHistory: ChatHistory
  ): Promise<void> => {
    const headers = {
      "Content-Type": "application/json",
      Accept: "text/event-stream",
    };
    const body = JSON.stringify(chatQuestion);

    try {
      const response = await fetchInstance.post(
        `/chat/${chatId}/question/stream`,
        body,
        headers
      );

      if (response.body === null) {
        throw new Error("Response body is null");
      }

      console.log("Received response. Starting to handle stream...");
      await handleStream(response.body.getReader(), chatHistory.message_id);
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
