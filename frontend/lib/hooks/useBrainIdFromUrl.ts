import { UUID } from "crypto";
import { useParams } from "next/navigation";

import { useBrainFetcher } from "@/app/brains-management/[brainId]/components/BrainManagementTabs/hooks/useBrainFetcher";

import { useBrainContext } from "../context/BrainProvider/hooks/useBrainContext";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useUrlBrain = () => {
  const { allBrains } = useBrainContext();

  const params = useParams();

  const brainId = params?.brainId as UUID | undefined;
  const correspondingBrain = allBrains.find((brain) => brain.id === brainId);

  const { brain: brainDetails, refetchBrain } = useBrainFetcher({
    brainId: brainId,
  });

  return {
    brain: correspondingBrain,
    brainId,
    brainDetails,
    refetchBrain,
  };
};
