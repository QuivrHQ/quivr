import { useFeature } from "@growthbook/growthbook-react";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useChatBar = () => {
  const shouldUseNewUX = useFeature("new-ux").on;

  return {
    shouldUseNewUX,
  };
};
