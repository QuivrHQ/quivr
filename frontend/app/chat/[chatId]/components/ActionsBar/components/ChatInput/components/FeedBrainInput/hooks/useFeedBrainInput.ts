import { useEffect } from "react";

import { requiredRolesForUpload } from "@/app/upload/config";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useFeedBrainInput = () => {
  const { currentBrain, setCurrentBrainId } = useBrainContext();
  useEffect(() => {
    if (
      currentBrain !== undefined &&
      !requiredRolesForUpload.includes(currentBrain.role)
    ) {
      setCurrentBrainId(null);
    }
  }, [currentBrain, setCurrentBrainId]);
};
