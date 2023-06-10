import { UUID } from "crypto";

export interface Chat {
  chatId: UUID;
  history: ChatHistory;
}

export type ChatMessage = [string, string];

export type ChatHistory = ChatMessage[];
