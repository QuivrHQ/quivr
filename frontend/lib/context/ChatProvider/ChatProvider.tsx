"use client";

import { createContext, useEffect, useState } from "react";

import { ChatItemWithGroupedNotifications } from "@/app/chat/[chatId]/components/ChatDialogueArea/types";
import { getMergedChatMessagesWithDoneStatusNotificationsReduced } from "@/app/chat/[chatId]/components/ChatDialogueArea/utils/getMergedChatMessagesWithDoneStatusNotificationsReduced";
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
  const [isLoadingHistoryChatItems, setIsLoadingHistoryChatItems] =
    useState<boolean>(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [sharedChatItems, setSharedChatItems] = useState<
    ChatItemWithGroupedNotifications[]
  >([]);

  const addToHistory = (message: ChatMessage) => {
    setMessages((prevHistory) => [...prevHistory, message]);
  };

  const updateStreamingHistory = (streamedChat: ChatMessage): void => {
    setMessages((prevHistory: ChatMessage[]) => {
      const updatedHistory = prevHistory.find(
        (item) => item.message_id === streamedChat.message_id
      )
        ? prevHistory.map((item: ChatMessage) =>
            item.message_id === streamedChat.message_id
              ? { ...item, assistant: item.assistant + streamedChat.assistant }
              : item
          )
        : [...prevHistory, streamedChat];

      return updatedHistory;
    });
  };

  const updateHistory = (chat: ChatMessage): void => {
    setMessages((prevHistory: ChatMessage[]) => {
      const updatedHistory = prevHistory.find(
        (item) => item.message_id === chat.message_id
      )
        ? prevHistory.map((item: ChatMessage) =>
            item.message_id === chat.message_id
              ? { ...item, assistant: chat.assistant }
              : item
          )
        : [...prevHistory, chat];

      return updatedHistory;
    });
  };

  useEffect(() => {
    if (messages.length > 0 || notifications.length > 0) {
      const chatItems = getMergedChatMessagesWithDoneStatusNotificationsReduced(
        messages,
        notifications
      );
      setSharedChatItems(chatItems);
    }
  }, [messages, notifications]);

  return (
    <ChatContext.Provider
      value={{
        messages,
        setMessages,
        addToHistory,
        updateHistory,
        updateStreamingHistory,
        notifications,
        setNotifications,
        sharedChatItems,
        setIsLoadingHistoryChatItems,
        isLoadingHistoryChatItems,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};
