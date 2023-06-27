/* eslint-disable max-lines */

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useState } from "react";

import { useAxios } from "@/lib/hooks";

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
  streamResponse: string;
}

export const useChatService = (): UseChatService => {
  const { axiosInstance } = useAxios();
  const { updateHistory } = useChatContext();
  const [streamResponse, setStreamResponse] = useState<string>("");
  const { currentBrain } = useBrainContext();
  const createChat = async ({
    name,
  }: {
    name: string;
  }): Promise<ChatEntity> => {
    return axiosInstance.post<ChatEntity>(`/chat`, { name });
  };

  const getChatHistory = async (
    chatId: string | undefined
  ): Promise<ChatHistory[]> => {
    if (chatId === undefined) {
      return [];
    }
    const rep = (
      await axiosInstance.get<ChatHistory[]>(`/chat/${chatId}/history`)
    ).data;

    return rep;
  };

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
    reader: ReadableStreamDefaultReader,
    chatHistory: ChatHistory
  ) => {
    const decoder = new TextDecoder("utf-8");
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      console.log("Reader status:", { done, value }); // log the status of the reader

      if (done || value === undefined) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });
      const payloads = buffer.split("\n\n");
      console.log("Payloads:", payloads); // log the payloads
      buffer = payloads.pop() as string;
      console.log("Buffer:", buffer); // log the buffer

      payloads
        .filter((payload) => payload.startsWith("data:"))
        .map((dataPayload) =>
          dataPayload.replace("data: ", "").replace("\n\n", "")
        )
        .forEach((data) => {
          console.log("Received data:", data);
          setStreamResponse(`${streamResponse}${data}`);
          updateHistory({ ...chatHistory, assistant: streamResponse });
        });
    }
  };

  const addStreamQuestion = async (
    chatId: string,
    chatQuestion: ChatQuestion,
    chatHistory: ChatHistory
  ): Promise<void> => {
    const url = `http://localhost:5050/chat/${chatId}/question/stream`;
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "text/event-stream",
        Authorization: "Bearer 27f13b64eb9ded70e241617fe01f0830",
      },
      body: JSON.stringify(chatQuestion),
    };

    setStreamResponse("");

    try {
      const response = await fetch(url, requestOptions);

      if (response.body === null) {
        throw new Error("Response body is null");
      }

      console.log("Received response. Starting to handle stream..."); // log when starting to handle the stream
      await handleStream(response.body.getReader(), chatHistory);
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
