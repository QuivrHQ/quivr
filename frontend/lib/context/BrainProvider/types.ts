import { UUID } from "crypto";

import { BrainRoleType } from "@/lib/components/BrainUsers/types";
import { Document } from "@/lib/types/Document";

import { useBrainProvider } from "./hooks/useBrainProvider";
import { Model } from "../../types/brainConfig";

export type BrainAccessStatus = "private" | "public";

export type Brain = {
  id: UUID;
  name: string;
  documents?: Document[];
  status?: BrainAccessStatus;
  model?: Model;
  max_tokens?: number;
  temperature?: number;
  openai_api_key?: string;
  description?: string;
  prompt_id?: string | null;
};

export type MinimalBrainForUser = {
  id: UUID;
  name: string;
  role: BrainRoleType;
  status: BrainAccessStatus;
};

//TODO: rename rights to role in Backend and use MinimalBrainForUser instead of BackendMinimalBrainForUser
export type BackendMinimalBrainForUser = Omit<MinimalBrainForUser, "role"> & {
  rights: BrainRoleType;
};

export type PublicBrain = {
  id: UUID;
  name: string;
  description?: string;
  number_of_subscribers: number;
  last_update: string;
};

export type BrainContextType = ReturnType<typeof useBrainProvider>;
