"use client";

import { createContext, useContext, useState } from "react";

import { ChatHistory } from "../types";

type ChatContextProps = {
  history: ChatHistory[];
  setHistory: (history: ChatHistory[]) => void;
  addToHistory: (message: ChatHistory) => void;
  updateHistory: (message_id: string, message: ChatHistory) => void;
  updateStreamingHistory: (
    message_id: string,
    assistantResponse: string
  ) => void;
};

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

  const updateStreamingHistory = (
    message_id: string,
    assistantResponse: string
  ): void => {
    setHistory((prevHistory: ChatHistory[]) => {
      const newHistory = prevHistory.map((item: ChatHistory) =>
        item.message_id === message_id
          ? { ...item, assistant: item.assistant + assistantResponse }
          : item
      );

      return newHistory;
    });
  };

  const updateHistory = (message_id: string, message: ChatHistory): void => {
    setHistory((prevHistory: ChatHistory[]) => {
      const newHistory = prevHistory.map((item: ChatHistory) =>
        item.message_id === message_id ? message : item
      );

      return newHistory;
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

export const useChatContext = (): ChatContextProps => {
  const context = useContext(ChatContext);

  if (context === undefined) {
    throw new Error("useChatContext must be used inside ChatProvider");
  }

  return context;
};
