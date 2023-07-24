import { Model, PaidModels } from "../context/BrainConfigProvider/types";

export const defineMaxTokens = (model: Model | PaidModels): number => {
  //At the moment is evaluating only models from OpenAI
  switch (model) {
    case "gpt-3.5-turbo-0613":
      return 500;
    case "gpt-3.5-turbo-16k":
      return 2000;
    case "gpt-4":
      return 1000;
    case "gpt-4-0613":
      return 100;
    default:
      return 250;
  }
};
