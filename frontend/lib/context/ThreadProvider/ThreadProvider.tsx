"use client";

import { createContext, useState } from "react";

import { Notification, ThreadMessage } from "@/app/thread/[threadId]/types";

import { ThreadContextProps } from "./types";

export const ThreadContext = createContext<ThreadContextProps | undefined>(
  undefined
);

export const ThreadProvider = ({
  children,
}: {
  children: JSX.Element | JSX.Element[];
}): JSX.Element => {
  const [messages, setMessages] = useState<ThreadMessage[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [sourcesMessageIndex, setSourcesMessageIndex] = useState<
    number | undefined
  >(undefined);

  const updateStreamingHistory = (streamedThread: ThreadMessage): void => {
    setMessages((prevHistory: ThreadMessage[]) => {
      const updatedHistory = prevHistory.find(
        (item) => item.message_id === streamedThread.message_id
      )
        ? prevHistory.map((item: ThreadMessage) =>
            item.message_id === streamedThread.message_id
              ? {
                  ...item,
                  assistant: item.assistant + streamedThread.assistant,
                  metadata: streamedThread.metadata,
                }
              : item
          )
        : [...prevHistory, streamedThread];

      return updatedHistory;
    });
  };

  const removeMessage = (id: string): void => {
    setMessages((prevHistory: ThreadMessage[]) =>
      prevHistory.filter((item) => item.message_id !== id)
    );
  };

  return (
    <ThreadContext.Provider
      value={{
        messages,
        setMessages,
        updateStreamingHistory,
        removeMessage,
        notifications,
        setNotifications,
        sourcesMessageIndex,
        setSourcesMessageIndex,
      }}
    >
      {children}
    </ThreadContext.Provider>
  );
};
