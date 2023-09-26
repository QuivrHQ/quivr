export const brainStatuses = ["private", "public"] as const;

export type BrainStatus = (typeof brainStatuses)[number];

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
  prompt_id?: string;
  status: BrainStatus;
  prompt: {
    title: string;
    content: string;
  };
  name: string;
  description: string;
  setDefault: boolean;
};

export type BrainConfigContextType = {
  config: BrainConfig;
};

export const openAiFreeModels = ["gpt-3.5-turbo", "gpt-3.5-turbo-16k"] as const;

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

export type Model = (typeof freeModels)[number];
