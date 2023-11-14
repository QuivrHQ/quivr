import { BrainRoleType } from "@/lib/components/BrainUsers/types";
import { BrainStatus, BrainType, Model } from "@/lib/types/brainConfig";

export type ApiBrainDefinitionSchemaProperty = {
  type: string;
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

export type ApiBrianDefinitionSecret = {
  name: string;
  type: string;
};

export type ApiBrainDefinition = {
  method: AllowedRequestMethod;
  url: string;
  searchParams: ApiBrainDefinitionSchema;
  params: ApiBrainDefinitionSchema;
  secrets: ApiBrianDefinitionSecret;
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
