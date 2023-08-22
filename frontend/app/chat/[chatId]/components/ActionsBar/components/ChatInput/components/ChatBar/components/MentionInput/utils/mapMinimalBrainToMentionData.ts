import { MentionData } from "@draft-js-plugins/mention";

import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

export const mapMinimalBrainToMentionData = (
  brain: MinimalBrainForUser
): MentionData => ({
  name: brain.name,
  id: brain.id as string,
  trigger: "@",
});
