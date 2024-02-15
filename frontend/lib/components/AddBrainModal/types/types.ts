import { CreateBrainInput } from "@/lib/api/brain/types";
import { iconList } from "@/lib/helpers/iconList";

const brainCreationSteps = ["BRAIN_TYPE", "BRAIN_PARAMS", "KNOWLEDGE"] as const;

export type BrainCreationStep = (typeof brainCreationSteps)[number];

export type CreateBrainProps = CreateBrainInput & {
  setDefault: boolean;
  brainCreationStep: BrainCreationStep;
};

export interface BrainType {
  name: string;
  description: string;
  iconName: keyof typeof iconList;
  disabled?: boolean;
  onClick?: () => void;
}

export type Step = {
  label: string;
  value: BrainCreationStep;
};
