import { BrainRoleType } from "@/lib/components/BrainUsers/types";
import { BrainStatus, BrainType } from "@/lib/types/brainConfig";

export type SubscriptionUpdatableProperties = {
  role: BrainRoleType | null;
};

export type CreateBrainInput = {
  name: string;
  description?: string;
  status?: BrainStatus;
  model?: string;
  temperature?: number;
  max_tokens?: number;
  openai_api_key?: string;
  prompt_id?: string | null;
  brain_type?: BrainType;
};

export type UpdateBrainInput = Partial<CreateBrainInput>;
