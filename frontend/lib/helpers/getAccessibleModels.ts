import { UserStats } from "@/lib/types/User";
import { freeModels, paidModels } from "@/lib/types/brainConfig";

type GetAccessibleModelsInput = {
  openAiKey?: string | null;
  userData?: UserStats;
};
export const getAccessibleModels = ({
  openAiKey,
  userData,
}: GetAccessibleModelsInput): string[] => {
  if (userData?.models !== undefined) {
    return userData.models;
  }
  if (openAiKey !== undefined && openAiKey !== null) {
    return paidModels as unknown as string[];
  }

  return freeModels as unknown as string[];
};
