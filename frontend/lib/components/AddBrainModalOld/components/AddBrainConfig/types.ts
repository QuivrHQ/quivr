import { CreateBrainInput } from "@/lib/api/brain/types";
import { CreatePromptProps } from "@/lib/api/prompt/prompt";

export type CreateBrainProps = CreateBrainInput & {
  prompt: CreatePromptProps;
  setDefault: boolean;
};
