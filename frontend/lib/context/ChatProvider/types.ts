import { ChatMessage, Notification } from "@/app/chat/[chatId]/types";

import { Model } from "../BrainConfigProvider/types";

export type ChatConfig = {
  model?: Model;
  temperature?: number;
  maxTokens?: number;
};

export type ChatContextProps = {
  messages: ChatMessage[];
  setMessages: (history: ChatMessage[]) => void;
  addToHistory: (message: ChatMessage) => void;
  updateHistory: (chat: ChatMessage) => void;
  updateStreamingHistory: (streamedChat: ChatMessage) => void;
  notifications: Notification[];
  setNotifications: (notifications: Notification[]) => void;
};
