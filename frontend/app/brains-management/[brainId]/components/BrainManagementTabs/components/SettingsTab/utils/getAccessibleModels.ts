import { UserStats } from "@/lib/types/User";
import { freeModels, paidModels } from "@/lib/types/brainConfig";

type GetAccessibleModelsInput = {
  openAiKey?: string;
  userData?: UserStats;
};
export const getAccessibleModels = ({
  openAiKey,
  userData,
}: GetAccessibleModelsInput): string[] => {
  if (userData?.models !== undefined) {
    return userData.models;
  }
  if (openAiKey !== undefined) {
    return paidModels as unknown as string[];
  }

  return freeModels as unknown as string[];
};
