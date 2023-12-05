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
    useState<boolean>(true);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [sharedChatItems, setSharedChatItems] = useState<
    ChatItemWithGroupedNotifications[]
  >([]);

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

  const removeMessage = (id: string): void => {
    setMessages((prevHistory: ChatMessage[]) =>
      prevHistory.filter((item) => item.message_id !== id)
    );
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
        updateStreamingHistory,
        removeMessage,
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
