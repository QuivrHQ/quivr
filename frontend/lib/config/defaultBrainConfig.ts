import { BrainConfig } from "../types/brainConfig";

export const defaultBrainConfig: BrainConfig = {
  model: "gpt-3.5-turbo",
  temperature: 0,
  maxTokens: 256,
  keepLocal: true,
  anthropicKey: undefined,
  backendUrl: undefined,
  openAiKey: undefined,
  supabaseKey: undefined,
  supabaseUrl: undefined,
  prompt_id: undefined,
  status: "private",
};
