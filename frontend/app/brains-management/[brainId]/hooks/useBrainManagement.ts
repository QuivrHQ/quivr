import { useUrlBrain } from "@/lib/hooks/useBrainIdFromUrl";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainManagement = () => {
  const { brain } = useUrlBrain();

  return {
    brain,
  };
};
