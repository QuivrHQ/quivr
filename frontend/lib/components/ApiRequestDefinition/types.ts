import { CreateBrainInput } from "@/lib/api/brain/types";

export const apiTabs = ["params", "searchParams", "secrets"] as const;

export type ApiTab = (typeof apiTabs)[number];

export type ApiDefinitionContextType = CreateBrainInput & {
  isApiDefinitionReadOnly?: boolean;
  isUpdatingApiDefinition?: boolean;
};
