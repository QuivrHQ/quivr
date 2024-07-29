"use client";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

interface BrainButtonProps {
  brain: MinimalBrainForUser;
}

const BrainButton = ({ brain }: BrainButtonProps): JSX.Element => {
  const { setCurrentBrainId } = useBrainContext();

  return <div onClick={() => setCurrentBrainId(brain.id)}>{brain.name}</div>;
};

export default BrainButton;
