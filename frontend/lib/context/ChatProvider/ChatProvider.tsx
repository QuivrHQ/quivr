"use client";

import { createContext, useState } from "react";

import { ChatMessage, Notification } from "@/app/chat/[chatId]/types";

import { ChatContextProps } from "./types";

export const ChatContext = createContext<ChatContextProps | undefined>(
  undefined
);

export const ChatProvider = ({
  children,
}: {
  children: JSX.Element | JSX.Element[];
}): JSX.Element => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const updateStreamingHistory = (streamedChat: ChatMessage): void => {
    setMessages((prevHistory: ChatMessage[]) => {
      const updatedHistory = prevHistory.find(
        (item) => item.message_id === streamedChat.message_id
      )
        ? prevHistory.map((item: ChatMessage) =>
            item.message_id === streamedChat.message_id
              ? {
                  ...item,
                  assistant: item.assistant + streamedChat.assistant,
                  metadata: streamedChat.metadata,
                }
              : item
          )
        : [...prevHistory, streamedChat];

      return updatedHistory;
    });
  };

  const removeMessage = (id: string): void => {
    setMessages((prevHistory: ChatMessage[]) =>
      prevHistory.filter((item) => item.message_id !== id)
    );
  };

  return (
    <ChatContext.Provider
      value={{
        messages,
        setMessages,
        updateStreamingHistory,
        removeMessage,
        notifications,
        setNotifications,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};
