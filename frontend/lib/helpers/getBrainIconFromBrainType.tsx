import { IconType } from "react-icons/lib";
import { LuBot, LuBrain } from "react-icons/lu";
import { PiPaperclipFill } from "react-icons/pi";
import { TbWorld } from "react-icons/tb";

import { BrainType } from "@/lib/types/brainConfig";
type GetBrainIconFromBrainTypeOptions = {
  iconSize?: number;
  ApiBrainIcon?: IconType;
  DocBrainIcon?: IconType;
};

export const getBrainIconFromBrainType = (
  brainType?: BrainType,
  options?: GetBrainIconFromBrainTypeOptions
): JSX.Element => {
  const iconSize = options?.iconSize ?? 38;

  const ApiBrainIcon = options?.ApiBrainIcon ?? TbWorld;
  const DocBrainIcon = options?.DocBrainIcon ?? PiPaperclipFill;

  if (brainType === undefined) {
    return <LuBrain size={iconSize} />;
  }
  if (brainType === "api") {
    return <ApiBrainIcon size={iconSize} />;
  }

  if (brainType === "composite") {
    return <LuBot size={iconSize} />;
  }

  return <DocBrainIcon size={iconSize} />;
};
