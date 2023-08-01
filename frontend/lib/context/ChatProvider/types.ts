import { ChatHistory } from "@/app/chat/[chatId]/types";

import { Model } from "../BrainConfigProvider/types";

export type ChatConfig = {
  model?: Model;
  temperature?: number;
  maxTokens?: number;
};

export type ChatContextProps = {
  history: ChatHistory[];
  setHistory: (history: ChatHistory[]) => void;
  addToHistory: (message: ChatHistory) => void;
  updateHistory: (chat: ChatHistory) => void;
  updateStreamingHistory: (streamedChat: ChatHistory) => void;
};
