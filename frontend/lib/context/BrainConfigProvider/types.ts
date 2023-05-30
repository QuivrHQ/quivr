export type BrainConfig = {
  model: Model;
  temperature: number;
  maxTokens: number;
  backendUrl?: string;
  openAiKey?: string;
  anthropicKey?: string;
  keepLocal: boolean;
  supabaseUrl?: string;
  supabaseKey?: string;
};

type OptionalConfig = { [K in keyof BrainConfig]?: BrainConfig[K] | undefined };

export type ConfigContext = {
  config: BrainConfig;
  updateConfig: (config: OptionalConfig) => void;
};

export const openAiModels = ["gpt-3.5-turbo", "gpt-4"] as const;

export const anthropicModels = [
  "claude-v1",
  "claude-v1.3",
  "claude-instant-v1-100k",
  "claude-instant-v1.1-100k",
] as const;

export const models = [...openAiModels, ...anthropicModels] as const;

export type Model = (typeof models)[number];
