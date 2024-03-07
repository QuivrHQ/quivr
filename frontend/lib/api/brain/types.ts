import { UUID } from "crypto";

import { BrainRoleType } from "@/app/studio/[brainId]/BrainManagementTabs/components/PeopleTab/BrainUsers/types";
import { BrainStatus, BrainType, Model } from "@/lib/types/BrainConfig";

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
  raw: boolean;
  jq_instructions: string;
};

export type IntegrationSettings = {
  integration_id?: string;
  settings?: { [x: string]: string | undefined };
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
  integration?: IntegrationSettings;
};

enum IntegrationBrainTag {
  NEW = "new",
  RECOMMENDED = "recommended",
  MOST_POPULAR = "most_popular",
  PREMIUM = "premium",
  COMING_SOON = "coming_soon",
  COMMUNITY = "community",
  DEPRECATED = "deprecated",
}

export type IntegrationBrains = {
  id: UUID;
  integration_name: string;
  integration_logo_url: string;
  connection_settings: string;
  integration_type: "custom" | "sync";
  description: string;
  max_files: number;
  tags: IntegrationBrainTag[];
  information: string;
  integration_display_name: string;
};

export type UpdateBrainInput = Partial<CreateBrainInput>;
