import { LuBrain } from "react-icons/lu";
import { PiPaperclipFill } from "react-icons/pi";
import { TbWorld } from "react-icons/tb";

import { BrainType } from "@/lib/types/brainConfig";

export const getKnowledgeCardIconFromBrainType = (
  brainType?: BrainType
): JSX.Element => {
  const iconSize = 38;
  if (brainType === undefined) {
    return <TbWorld size={iconSize} />;
  }
  if (brainType === "api") {
    return <LuBrain size={iconSize} />;
  }

  return <PiPaperclipFill size={iconSize} />;
};
