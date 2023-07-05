"use client";

import { createContext, useState } from "react";

import { ChatHistory } from "@/app/chat/[chatId]/types";

import { ChatContextProps } from "./types";

export const ChatContext = createContext<ChatContextProps | undefined>(
  undefined
);

export const ChatProvider = ({
  children,
}: {
  children: JSX.Element | JSX.Element[];
}): JSX.Element => {
  const [history, setHistory] = useState<ChatHistory[]>([]);

  const addToHistory = (message: ChatHistory) => {
    setHistory((prevHistory) => [...prevHistory, message]);
  };

  const updateStreamingHistory = (streamedChat: ChatHistory): void => {
    setHistory((prevHistory: ChatHistory[]) => {
      const updatedHistory = prevHistory.find(
        (item) => item.message_id === streamedChat.message_id
      )
        ? prevHistory.map((item: ChatHistory) =>
            item.message_id === streamedChat.message_id
              ? { ...item, assistant: item.assistant + streamedChat.assistant }
              : item
          )
        : [...prevHistory, streamedChat];

      return updatedHistory;
    });
  };

  const updateHistory = (chat: ChatHistory): void => {
    setHistory((prevHistory: ChatHistory[]) => {
      const updatedHistory = prevHistory.find(
        (item) => item.message_id === chat.message_id
      )
        ? prevHistory.map((item: ChatHistory) =>
            item.message_id === chat.message_id
              ? { ...item, assistant: chat.assistant }
              : item
          )
        : [...prevHistory, chat];

      return updatedHistory;
    });
  };

  return (
    <ChatContext.Provider
      value={{
        history,
        setHistory,
        addToHistory,
        updateHistory,
        updateStreamingHistory,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};
