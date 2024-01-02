import { useTranslation } from "react-i18next";
import { IconType } from "react-icons/lib";
import { LuBot, LuFilePlus, LuUnlock } from "react-icons/lu";

import { BrainType } from "@/lib/types/brainConfig";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useFeedCardTriggerUtils = () => {
  const { t } = useTranslation(["chat", "brain"]);

  const brainTypeToLabel: Record<BrainType, string> = {
    doc: t("chat:add_document"),
    api: t("brain:update_secrets_button"),
    composite: t("brain:manage_brain"),
  };

  const brainTypeToIcon: Record<BrainType, IconType> = {
    doc: LuFilePlus,
    api: LuUnlock,
    composite: LuBot,
  };

  return {
    brainTypeToIcon,
    brainTypeToLabel,
  };
};
