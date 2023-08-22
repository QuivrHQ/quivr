import { MentionData } from "@draft-js-plugins/mention";

import { MentionTriggerType } from "../../../../types";

export type MentionInputMentionsType = Record<
  MentionTriggerType,
  MentionData[]
>;

export type TriggerMap = {
  trigger: MentionTriggerType;
  content: string;
};
