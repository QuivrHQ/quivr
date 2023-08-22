import { MentionData } from "@draft-js-plugins/mention";

import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

export const mapMinimalBrainToMentionData = (
  brains: MinimalBrainForUser[]
): MentionData[] =>
  brains.map((brain) => ({
    name: brain.name,
    id: brain.id as string,
  }));
