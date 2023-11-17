import { UUID } from "crypto";

import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

import { isUserBrainOwner } from "./isUserBrainEditor";
import { isUserBrainEditor } from "./isUserBrainOwner";

type GetBrainPermissionsProps = {
  brainId?: UUID;
  userAccessibleBrains: MinimalBrainForUser[];
};

export const getBrainPermissions = ({
  brainId,
  userAccessibleBrains,
}: GetBrainPermissionsProps): {
  isPublicBrain: boolean;
  hasEditRights: boolean;
  isOwnedByCurrentUser: boolean;
} => {
  const isOwnedByCurrentUser = isUserBrainOwner({
    brainId,
    userAccessibleBrains,
  });

  const userHasBrainEditorRights = isUserBrainEditor({
    brainId,
    userAccessibleBrains,
  });

  const isPublicBrain =
    userAccessibleBrains.find((brain) => brain.id === brainId)?.status ===
    "public";

  const hasEditRights = isOwnedByCurrentUser || userHasBrainEditorRights;

  return { isPublicBrain, hasEditRights, isOwnedByCurrentUser };
};
