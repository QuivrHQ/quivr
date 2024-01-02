import { CreateBrainInput } from "@/lib/api/brain/types";

const brainCreationSteps = ["BRAIN_TYPE", "BRAIN_PARAMS", "KNOWLEDGE"] as const;

export type BrainCreationStep = (typeof brainCreationSteps)[number];

export type CreateBrainProps = CreateBrainInput & {
  setDefault: boolean;
  brainCreationStep: BrainCreationStep;
};
