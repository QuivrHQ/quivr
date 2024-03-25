import { UUID } from "crypto";
import { useEffect } from "react";
import { useFormContext } from "react-hook-form";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { getBrainPermissions } from "../../../utils/getBrainPermissions";

type UsePermissionsControllerProps = {
  brainId: UUID;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const usePermissionsController = ({
  brainId,
}: UsePermissionsControllerProps) => {
  const { allBrains } = useBrainContext();

  const { setValue } = useFormContext<{
    isApiDefinitionReadOnly: boolean;
    isUpdatingApiDefinition: boolean;
  }>();

  const { hasEditRights, isOwnedByCurrentUser } = getBrainPermissions({
    brainId,
    userAccessibleBrains: allBrains,
  });

  useEffect(() => {
    setValue("isApiDefinitionReadOnly", !hasEditRights);
    setValue("isUpdatingApiDefinition", true);
  }, [hasEditRights, setValue]);

  return {
    hasEditRights,
    isOwnedByCurrentUser,
  };
};
