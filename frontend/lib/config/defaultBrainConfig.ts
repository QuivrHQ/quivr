import { CreateBrainInput } from "../api/brain/types";
import { Model } from "../types/BrainConfig";

export const addBrainDefaultValues: CreateBrainInput = {
  model: "gpt-3.5-turbo",
  temperature: 0,
  max_tokens: 1000,
  prompt_id: undefined,
  status: "private",
  name: "",
  description: "",
  brain_type: "doc",
  brain_definition: {
    method: "GET",
    url: "",
    search_params: {
      properties: [],
      required: [],
    },
    params: {
      properties: [],
      required: [],
    },
    secrets: [],
    raw: false,
    jq_instructions: "",
  },
  connected_brains_ids: [],
  integration: undefined,
};

export const defaultModel: Model = "gpt-3.5-turbo";
export const defaultMaxTokens = 1000;
export const defaultTemperature = 0;
