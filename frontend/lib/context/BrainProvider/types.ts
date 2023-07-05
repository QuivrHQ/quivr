import { UUID } from "crypto";

import { Document } from "@/lib/types/Document";

import { useBrainState } from "./hooks/useBrainState";

export type Brain = {
  id: UUID;
  name: string;
  documents?: Document[];
  status?: string;
  model?: string;
  max_tokens?: string;
  temperature?: string;
};

export type BrainContextType = ReturnType<typeof useBrainState>;
