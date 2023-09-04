import { MentionData } from "@draft-js-plugins/mention";

import { Prompt } from "@/lib/types/Prompt";

export const mapPromptToMentionData = (prompt: Prompt): MentionData => ({
  name: prompt.title,
  id: prompt.id,
  trigger: "#",
});
