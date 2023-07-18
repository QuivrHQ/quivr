import { UUID } from "crypto";

import { BrainRoleType } from "@/lib/components/NavBar/components/NavItems/components/BrainsDropDown/components/BrainActions/types";
import { Document } from "@/lib/types/Document";

import { useBrainProvider } from "./hooks/useBrainProvider";

export type Brain = {
  id: UUID;
  name: string;
  documents?: Document[];
  status?: string;
  model?: string;
  max_tokens?: string;
  temperature?: string;
};

export type MinimalBrainForUser = {
  id: UUID;
  name: string;
  rights: BrainRoleType;
};

export type BrainContextType = ReturnType<typeof useBrainProvider>;
