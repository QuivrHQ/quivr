import { UUID } from "crypto";

export type BrainConfig = {
  model: Model;
  temperature: number;
  maxTokens: number;
  keepLocal: boolean;
  backendUrl?: string;
  openAiKey?: string;
  anthropicKey?: string;
  supabaseUrl?: string;
  supabaseKey?: string;
  prompt_id?: UUID;
};

type OptionalConfig = { [K in keyof BrainConfig]?: BrainConfig[K] | undefined };

export type BrainConfigContextType = {
  config: BrainConfig;
  updateConfig: (config: OptionalConfig) => void;
  resetConfig: () => void;
};

// export const openAiModels = ["gpt-3.5-turbo", "gpt-4"] as const; ## TODO activate GPT4 when not in demo mode

export const openAiModels = [
  "gpt-3.5-turbo",
  "gpt-3.5-turbo-0613",
  "gpt-3.5-turbo-16k",
] as const;
export const openAiPaidModels = [
  "gpt-3.5-turbo-0613",
  "gpt-3.5-turbo-16k",
  "gpt-4",
  "gpt-4-0613",
] as const;

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
export const models = [
  ...openAiModels,
  ...anthropicModels,
  ...googleModels,
] as const;

export const paidModels = [...openAiPaidModels] as const;

export type PaidModels = (typeof paidModels)[number];

export type Model = (typeof models)[number];
