import { Fragment } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { useFeedCardTriggerUtils } from "./useFeedCardTriggerUtils";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useFeedCardTrigger = () => {
  const { brainTypeToIcon, brainTypeToLabel } = useFeedCardTriggerUtils();
  const { currentBrain } = useBrainContext();

  const isBrainTypeDefined = currentBrain?.brain_type !== undefined;

  return {
    label: isBrainTypeDefined ? brainTypeToLabel[currentBrain.brain_type] : "",
    Icon: isBrainTypeDefined
      ? brainTypeToIcon[currentBrain.brain_type]
      : Fragment,
  };
};
