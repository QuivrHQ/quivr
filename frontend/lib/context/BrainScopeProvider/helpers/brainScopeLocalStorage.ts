import { BrainScope } from "../types";

const BRAIN_SCOPE_LOCAL_STORAGE_KEY = "userBrainConfig";

export const saveBrainScopeInLocalStorage = (updatedConfig: BrainScope) => {
  localStorage.setItem(
    BRAIN_SCOPE_LOCAL_STORAGE_KEY,
    JSON.stringify(updatedConfig)
  );
};
export const getBrainFromLocalStorage = (): BrainScope | undefined => {
  const persistedBrainConfig = localStorage.getItem(
    BRAIN_SCOPE_LOCAL_STORAGE_KEY
  );
  if (persistedBrainConfig === null) return;
  return JSON.parse(persistedBrainConfig);
};
