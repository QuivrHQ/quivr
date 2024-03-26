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

  const hasEditRights = isOwnedByCurrentUser || userHasBrainEditorRights;

  return {
    hasEditRights,
    isOwnedByCurrentUser,
  };
};
