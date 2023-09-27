import { UUID } from "crypto";

import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

import { isUserBrainOwner } from "./isUserBrainOwner";

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

  const isPublicBrain =
    userAccessibleBrains.find((brain) => brain.id === brainId)?.status ===
    "public";

  const hasEditRights = !isPublicBrain || isOwnedByCurrentUser;

  return { isPublicBrain, hasEditRights, isOwnedByCurrentUser };
};
