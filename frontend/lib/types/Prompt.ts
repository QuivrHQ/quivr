import { UUID } from "crypto";

export type Prompt = {
  id: UUID;
  title: string;
  content: string;
};
