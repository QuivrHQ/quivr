import { UUID } from "crypto";

export interface Chat {
  chatId: UUID;
  chatName: string;
  history: Array<[string, string]>;
}
