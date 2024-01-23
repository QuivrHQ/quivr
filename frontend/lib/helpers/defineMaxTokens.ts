import { Model, PaidModels } from "../types/BrainConfig";

export const defineMaxTokens = (
  model: Model | PaidModels | undefined
): number => {
  //At the moment is evaluating only models from OpenAI
  switch (model) {
    case "gpt-3.5-turbo":
      return 2000;
    case "gpt-3.5-turbo-1106":
      return 2000;
    case "gpt-3.5-turbo-16k":
      return 4000;
    case "gpt-4":
      return 4000;
    default:
      return 1000;
  }
};
