import { CreateBrainInput } from "../api/brain/types";
import { BrainConfig } from "../types/brainConfig";

export const addBrainDefaultValues: CreateBrainInput = {
  model: "gpt-3.5-turbo",
  temperature: 0,
  max_tokens: 500,
  openai_api_key: undefined,
  prompt_id: undefined,
  status: "private",
  name: "",
  description: "",
  brain_type: "doc",
};

export const defaultBrainConfig: BrainConfig = {
  model: "gpt-3.5-turbo",
  temperature: 0,
  maxTokens: 500,
  keepLocal: true,
  anthropicKey: undefined,
  backendUrl: undefined,
  openAiKey: undefined,
  supabaseKey: undefined,
  supabaseUrl: undefined,
  prompt_id: undefined,
  status: "private",
  prompt: {
    title: "",
    content: "",
  },
  name: "",
  description: "",
  setDefault: false,
  brain_type: "doc",
};
