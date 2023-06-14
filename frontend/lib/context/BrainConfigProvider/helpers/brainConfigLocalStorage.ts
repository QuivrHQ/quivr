/* eslint-disable */
import { BrainConfig } from "../types";

const BRAIN_CONFIG_LOCAL_STORAGE_KEY = "userBrainConfig";

export const saveBrainConfigInLocalStorage = (updatedConfig: BrainConfig) => {
  localStorage.setItem(
    BRAIN_CONFIG_LOCAL_STORAGE_KEY,
    JSON.stringify(updatedConfig)
  );
};
export const getBrainConfigFromLocalStorage = (): BrainConfig | undefined => {
  const persistedBrainConfig = localStorage.getItem(
    BRAIN_CONFIG_LOCAL_STORAGE_KEY
  );
  if (persistedBrainConfig === null) {
    return;
  }

  return JSON.parse(persistedBrainConfig);
};
