import { UUID } from "crypto";

export interface Chat {
  chatId: UUID;
  chatName: string;
  history: ChatHistory;
}
export type ChatMessage = [string, string];

export type ChatHistory = ChatMessage[];

  export type ChatResponse = Omit<Chat, "chatId"> & {
    chatId: UUID | undefined;
  };
