import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

import { MentionTriggerType } from "../../../../types";

export type MentionInputMentionsType = {
  "@": MinimalBrainForUser[];
};
export type TriggerMap = {
  trigger: MentionTriggerType;
  content: string;
};
