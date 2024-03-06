import { getThreadsConfigFromLocalStorage } from "@/lib/api/thread/thread.local.ts";
import { useUserData } from "@/lib/hooks/useUserData";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useLocalStorageThreadConfig = () => {
  const { userData } = useUserData();

  const threadConfig = getThreadsConfigFromLocalStorage();

  const model = (userData?.models ?? []).includes(threadConfig?.model ?? "")
    ? threadConfig?.model
    : undefined;

  return {
    threadConfig: {
      model: model,
      temperature: threadConfig?.temperature,
      maxTokens: threadConfig?.maxTokens,
    },
  };
};
