import { UUID } from "crypto";

import { BrainRoleType } from "@/lib/components/BrainUsers/types";
import { BrainStatus, BrainType, Model } from "@/lib/types/brainConfig";

export type ApiBrainDefinitionSchemaPropertyType = "string" | "number";

export type ApiBrainDefinitionSchemaProperty = {
  type: ApiBrainDefinitionSchemaPropertyType;
  description: string;
  name: string;
};
export const allowedRequestMethods = ["GET", "POST", "PUT", "DELETE"] as const;

export type AllowedRequestMethod = (typeof allowedRequestMethods)[number];

export type ApiBrainDefinitionSchema = {
  properties: ApiBrainDefinitionSchemaProperty[];
  required: string[];
};

export type SubscriptionUpdatableProperties = {
  role: BrainRoleType | null;
};

export type ListFilesProps = {
  files: {
      file_name: string;
      file_sha1: string;
      file_size: number;
      file_url: string;
      file_id: string;
      file_similarity: number;
  }[];
};

export type ApiBrainDefinitionSecret = {
  name: string;
  type: ApiBrainDefinitionSchemaPropertyType;
  description: string;
};

export type ApiBrainDefinition = {
  brain_id: UUID;
  method: AllowedRequestMethod;
  url: string;
  search_params: ApiBrainDefinitionSchema;
  params: ApiBrainDefinitionSchema;
  secrets?: ApiBrainDefinitionSecret[];
};

export type CreateBrainInput = {
  name: string;
  description: string;
  status?: BrainStatus;
  model?: Model;
  temperature?: number;
  max_tokens?: number;
  prompt_id?: string | null;
  brain_type?: BrainType;
  brain_definition?: Omit<ApiBrainDefinition, "brain_id">;
  brain_secrets_values?: Record<string, string>;
  connected_brains_ids?: UUID[];
};

export type UpdateBrainInput = Partial<CreateBrainInput>;
