import { Document } from "@/app/explore/types";
import _useBrainScopeState from "./hooks/_useBrainScopeState";

export type BrainScope = {
  id: string;
  name: string;
  documents: Document[];
};

export type ScopeContext = ReturnType<typeof _useBrainScopeState>;
