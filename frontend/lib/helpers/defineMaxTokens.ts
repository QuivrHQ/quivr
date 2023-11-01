import { Model, PaidModels } from "../types/brainConfig";

export const defineMaxTokens = (model: Model | PaidModels): number => {
  //At the moment is evaluating only models from OpenAI
  switch (model) {
    case "gpt-3.5-turbo":
      return 1000;
    case "gpt-3.5-turbo-16k":
      return 4000;
    case "gpt-4":
      return 4000;
    default:
      return 500;
  }
};
