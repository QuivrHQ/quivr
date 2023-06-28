import { Brain } from "../types";

const BRAIN_LOCAL_STORAGE_KEY = "userBrains";

export const saveBrainInLocalStorage = (brain: Brain): void => {
  localStorage.setItem(BRAIN_LOCAL_STORAGE_KEY, JSON.stringify(brain));
};
export const getBrainFromLocalStorage = (): Brain | undefined => {
  const persistedBrain = localStorage.getItem(BRAIN_LOCAL_STORAGE_KEY);
  if (persistedBrain === null) {
    return;
  }

  return JSON.parse(persistedBrain) as Brain;
};
