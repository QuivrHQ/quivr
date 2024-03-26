import { Model, PaidModels } from "../types/BrainConfig";

export const defineMaxTokens = (
  model: Model | PaidModels | undefined
): number => {
  // At the moment is evaluating only models from OpenAI
  switch (model) {
    case "gpt-3.5-turbo":
      return 2000;
    case "gpt-4":
      return 4000;
    case "gpt-4-turbo-preview":
      return 4000;
    case "mistral/mistral-small":
      return 1000;
    case "mistral/mistral-medium":
      return 2000;
    case "mistral/mistral-large-latest":
      return 2000;
    default:
      return 1000;
  }
};
