import { UUID } from "crypto";

import { BrainRoleType } from "@/lib/components/NavBar/components/NavItems/components/BrainsDropDown/components/BrainActions/types";
import { Document } from "@/lib/types/Document";

import { useBrainProvider } from "./hooks/useBrainProvider";
import { Model } from "../BrainConfigProvider/types";

export type Brain = {
  id: UUID;
  name: string;
  documents?: Document[];
  status?: string;
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
};

//TODO: rename rights to role in Backend and use MinimalBrainForUser instead of BackendMinimalBrainForUser
export type BackendMinimalBrainForUser = Omit<MinimalBrainForUser, "role"> & {
  rights: BrainRoleType;
};

export type BrainContextType = ReturnType<typeof useBrainProvider>;
