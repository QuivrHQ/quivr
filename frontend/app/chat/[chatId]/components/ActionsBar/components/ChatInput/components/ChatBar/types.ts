import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

export type BrainMentionType = MinimalBrainForUser & { value: string };

export type Trigger = "@" | "#";

export type BrainMentionsList = {
  "@": MinimalBrainForUser[];
};
