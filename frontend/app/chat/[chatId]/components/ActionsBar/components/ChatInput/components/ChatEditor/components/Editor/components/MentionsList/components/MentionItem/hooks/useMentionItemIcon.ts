import { CgFileDocument } from "react-icons/cg";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { getBrainIconFromBrainType } from "@/lib/helpers/getBrainIconFromBrainType";

import { SuggestionDataType, SuggestionItem } from "../../../../../types";

type UseBrainIcon = {
  item: SuggestionItem;
  type: SuggestionDataType;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useMentionItemIcon = ({ item, type }: UseBrainIcon) => {
  const isBrain = type === "brain";

  const { allBrains } = useBrainContext();
  const brain = isBrain ? allBrains.find((b) => b.id === item.id) : undefined;

  if (brain === undefined) {
    return {
      icon: undefined,
    };
  }

  return {
    icon: getBrainIconFromBrainType(brain.brain_type, {
      iconSize: 24,
      DocBrainIcon: CgFileDocument,
    }),
  };
};
