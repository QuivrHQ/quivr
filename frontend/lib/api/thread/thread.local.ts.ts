import { ThreadConfig } from "@/lib/context/ThreadProvider/types";
const threadConfigLocalStorageKey = "thread-config";

type PartialThreadConfig = Partial<ThreadConfig>;

export const saveThreadsConfigInLocalStorage = (
  threadConfig: PartialThreadConfig
): void => {
  localStorage.setItem(
    threadConfigLocalStorageKey,
    JSON.stringify(threadConfig)
  );
};

export const getThreadsConfigFromLocalStorage = ():
  | PartialThreadConfig
  | undefined => {
  try {
    const config = localStorage.getItem(threadConfigLocalStorageKey);

    if (config === null) {
      return undefined;
    }

    return JSON.parse(config) as PartialThreadConfig;
  } catch (error) {
    return undefined;
  }
};
