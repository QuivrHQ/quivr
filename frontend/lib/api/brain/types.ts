import { BrainRoleType } from "@/lib/components/BrainUsers/types";
import { BrainStatus, BrainType, Model } from "@/lib/types/brainConfig";

export type ApiBrainDefinitionSchemaPropertyType = "string" | "number";

export type ApiBrainDefinitionSchemaProperty = {
  type: ApiBrainDefinitionSchemaPropertyType;
  description: string;
  name: string;
};
export const allowedRequestMethods = ["GET", "POST", "PUT", "DELETE"];

export type AllowedRequestMethod = (typeof allowedRequestMethods)[number];

export type ApiBrainDefinitionSchema = {
  properties: ApiBrainDefinitionSchemaProperty[];
  required: string[];
};

export type SubscriptionUpdatableProperties = {
  role: BrainRoleType | null;
};

export type ApiBrainDefinitionSecret = {
  name: string;
  type: ApiBrainDefinitionSchemaPropertyType;
  description: string;
};

export type ApiBrainDefinition = {
  method: AllowedRequestMethod;
  url: string;
  search_params: ApiBrainDefinitionSchema;
  params: ApiBrainDefinitionSchema;
  secrets?: ApiBrainDefinitionSecret[];
};

export type CreateBrainInput = {
  name: string;
  description?: string;
  status?: BrainStatus;
  model?: Model;
  temperature?: number;
  max_tokens?: number;
  openai_api_key?: string;
  prompt_id?: string | null;
  brain_type?: BrainType;
  brain_definition?: ApiBrainDefinition;
  brain_secrets_values?: Record<string, string>;
};

export type UpdateBrainInput = Partial<CreateBrainInput>;
