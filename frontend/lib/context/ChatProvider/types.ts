import { ChatHistory } from "@/app/chat/[chatId]/types";

export type ChatContextProps = {
  history: ChatHistory[];
  setHistory: (history: ChatHistory[]) => void;
  addToHistory: (message: ChatHistory) => void;
  updateHistory: (chat: ChatHistory) => void;
  updateStreamingHistory: (streamedChat: ChatHistory) => void;
};
