import { Brain } from "../types";

const BRAIN_LOCAL_STORAGE_KEY = "userBrains";

export const saveBrainInLocalStorage = (updatedConfig: Brain): void => {
  localStorage.setItem(BRAIN_LOCAL_STORAGE_KEY, JSON.stringify(updatedConfig));
};
export const getBrainFromLocalStorage = (): Brain | undefined => {
  const persistedBrain = localStorage.getItem(BRAIN_LOCAL_STORAGE_KEY);
  if (persistedBrain === null) {
    return;
  }

  return JSON.parse(persistedBrain) as Brain;
};
