import { UUID } from "crypto";

export interface Chat {
  chatId: UUID;
  chatName: string;
  history: ChatHistory;
}
export type ChatMessage = [string, string];

export type ChatHistory = ChatMessage[];
