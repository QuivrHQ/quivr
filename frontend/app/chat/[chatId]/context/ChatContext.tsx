"use client";

import { createContext, useContext, useState } from "react";

import { ChatHistory } from "../types";

type ChatContextProps = {
  history: ChatHistory[];
  setHistory: (history: ChatHistory[]) => void;
  addToHistory: (message: ChatHistory) => void;
  setDocRetrieval: (docRetrieval: boolean) => void;
  docRetrieval: boolean;
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
  const [docRetrieval, setDocRetrieval] = useState<boolean>(false);

  return (
    <ChatContext.Provider
      value={{
        history,
        setHistory,
        addToHistory,
        docRetrieval,
        setDocRetrieval,
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
