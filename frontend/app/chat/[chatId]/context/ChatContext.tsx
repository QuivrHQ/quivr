"use client";

import { createContext, useContext, useState } from "react";

import { ChatHistory } from "../types";

type ChatContextProps = {
  history: ChatHistory[];
  setHistory: (history: ChatHistory[]) => void;
  addToHistory: (message: ChatHistory) => void;
  updateHistory: (message: ChatHistory) => void;
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

  const updateHistory = (message: ChatHistory) => {
    console.log("updateHistory", message);
    setHistory(
      history.map((item) => (item.chat_id === message.chat_id ? message : item))
    );
    console.log("updateHistory", history);
  };

  return (
    <ChatContext.Provider
      value={{
        history,
        setHistory,
        addToHistory,
        updateHistory,
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
