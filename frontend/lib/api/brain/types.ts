import { BrainRoleType } from "@/lib/components/NavBar/components/NavItems/components/BrainsDropDown/components/BrainActions/types";

export type SubscriptionUpdatableProperties = {
  role: BrainRoleType | null;
};

export type CreateBrainInput = {
  name: string;
  description?: string;
  status?: string;
  model?: string;
  temperature?: number;
  max_tokens?: number;
  openai_api_key?: string;
  prompt_id?: string | null;
};

export type UpdateBrainInput = Partial<CreateBrainInput>;
