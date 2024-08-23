import { UUID } from "crypto";

import { ApiBrainDefinition } from "../api/brain/types";

export const brainStatuses = ["private", "public"] as const;

export const brainTypes = [
  "doc",
  "api",
  "composite",
  "integration",
  "model",
] as const;

export type BrainType = (typeof brainTypes)[number];

export type BrainStatus = (typeof brainStatuses)[number];

export type Model = (typeof freeModels)[number];

// TODO: update this type to match the backend (antropic, openai and some other keys should be removed)
export type BrainConfig = {
  id: UUID;
  model: Model;
  temperature: number;
  maxTokens: number;
  keepLocal: boolean;
  backendUrl?: string;
  openAiKey?: string;
  anthropicKey?: string;
  supabaseUrl?: string;
  supabaseKey?: string;
  prompt_id?: string;
  status: BrainStatus;
  brain_type: BrainType;
  prompt: {
    title: string;
    content: string;
  };
  name: string;
  description: string;
} & {
  brain_definition?: ApiBrainDefinition;
};

export const openAiFreeModels = [
  "gpt-3.5-turbo",
  "gpt-4o",
  "gpt-3.5-turbo-1106",
  "gpt-3.5-turbo-16k",
  "gpt-4-0125-preview",
  "gpt-3.5-turbo-0125",
  "mistral/mistral-small",
  "mistral/mistral-medium",
  "mistral/mistral-large-latest",
] as const;

export const openAiPaidModels = [...openAiFreeModels, "gpt-4"] as const;

export const anthropicModels = [
  // "claude-v1",
  // "claude-v1.3",
  // "claude-instant-v1-100k",
  // "claude-instant-v1.1-100k",
] as const;

export const googleModels = [
  //"vertexai"
] as const; // TODO activate when not in demo mode

// export const googleModels = [] as const;
export const freeModels = [
  ...openAiFreeModels,
  // ...anthropicModels,
  // ...googleModels,
] as const;

export const paidModels = [...openAiPaidModels] as const;

export type PaidModels = (typeof paidModels)[number];
