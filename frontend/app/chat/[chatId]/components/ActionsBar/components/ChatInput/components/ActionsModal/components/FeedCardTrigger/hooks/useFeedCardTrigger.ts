import { useTranslation } from "react-i18next";
import { LuFilePlus } from "react-icons/lu";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { useFeedCardTriggerUtils } from "./useFeedCardTriggerUtils";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useFeedCardTrigger = () => {
  const { t } = useTranslation(["chat", "brain"]);

  const feedCardButtonDefaultLabel = t("chat:add_document");
  const feedCardButtonDefaultIcon = LuFilePlus;
  const { brainTypeToIcon, brainTypeToLabel } = useFeedCardTriggerUtils();
  const { currentBrain } = useBrainContext();

  const isBrainTypeDefined = currentBrain?.brain_type !== undefined;

  return {
    label: isBrainTypeDefined
      ? brainTypeToLabel[currentBrain.brain_type]
      : feedCardButtonDefaultLabel,
    Icon: isBrainTypeDefined
      ? brainTypeToIcon[currentBrain.brain_type]
      : feedCardButtonDefaultIcon,
  };
};
