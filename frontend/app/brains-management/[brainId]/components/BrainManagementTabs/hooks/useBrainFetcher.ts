import { useQuery } from "@tanstack/react-query";
import { UUID } from "crypto";
import { useRouter } from "next/navigation";

import { getBrainDataKey } from "@/lib/api/brain/config";
import { useBrainApi } from "@/lib/api/brain/useBrainApi";

type UseBrainFetcherProps = {
  brainId?: UUID;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainFetcher = ({ brainId }: UseBrainFetcherProps) => {
  const { getBrain } = useBrainApi();
  const router = useRouter();

  const fetchBrain = async () => {
    try {
      if (brainId === undefined) {
        return undefined;
      }

      return await getBrain(brainId);
    } catch (error) {
      console.log("error", error);
      router.push("/brains-management");
    }
  };

  console.log("brainId", brainId);
  const { data: brain } = useQuery({
    queryKey: [getBrainDataKey(brainId!)],
    queryFn: fetchBrain,
    enabled: brainId !== undefined,
  });
  console.log("QUERY DATA", brain);

  return {
    brain,
  };
};
