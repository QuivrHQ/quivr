import { UUID } from "crypto";

export interface Chat {
  chatId: UUID;
  history: Array<[string, string]>;
}
