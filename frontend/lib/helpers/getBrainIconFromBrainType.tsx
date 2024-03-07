import { IconType } from "react-icons/lib";
import { LuBot, LuBrain } from "react-icons/lu";
import { PiPaperclipFill } from "react-icons/pi";
import { TbWorld } from "react-icons/tb";

import { BrainType } from "@/lib/types/BrainConfig";
type GetBrainIconFromBrainTypeOptions = {
  iconSize?: number;
  ApiBrainIcon?: IconType;
  DocBrainIcon?: IconType;
  iconClassName?: string;
};

export const getBrainIconFromBrainType = (
  brainType?: BrainType,
  options?: GetBrainIconFromBrainTypeOptions
): JSX.Element => {
  const iconSize = options?.iconSize ?? 38;

  const ApiBrainIcon = options?.ApiBrainIcon ?? TbWorld;
  const DocBrainIcon = options?.DocBrainIcon ?? PiPaperclipFill;

  if (brainType === undefined) {
    return <LuBrain size={iconSize} className={options?.iconClassName} />;
  }
  if (brainType === "api") {
    return <ApiBrainIcon size={iconSize} className={options?.iconClassName} />;
  }

  if (brainType === "composite") {
    return <LuBot size={iconSize} className={options?.iconClassName} />;
  }

  return <DocBrainIcon size={iconSize} className={options?.iconClassName} />;
};
