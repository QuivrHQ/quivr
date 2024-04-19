import { CreateBrainInput } from "@/lib/api/brain/types";
import { iconList } from "@/lib/helpers/iconList";

const steps = ["FIRST_STEP", "SECOND_STEP", "THIRD_STEP"] as const;

export type StepValue = (typeof steps)[number];

export type CreateBrainProps = CreateBrainInput & {
  setDefault: boolean;
  brainCreationStep: StepValue;
};

export interface BrainType {
  name: string;
  description: string;
  iconName: keyof typeof iconList;
  disabled?: boolean;
  onClick?: () => void;
}
