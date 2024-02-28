"use client";
import { UUID } from "crypto";

import { ApiBrainSecretsInputs } from "@/lib/components/ApiBrainSecretsInputs/ApiBrainSecretsInputs";

import { AddedKnowledge } from "./components/AddedKnowledge/AddedKnowledge";

import { useBrainFetcher } from "../../hooks/useBrainFetcher";

type KnowledgeTabProps = {
  brainId: UUID;
  hasEditRights: boolean;
};
export const KnowledgeTab = ({ brainId }: KnowledgeTabProps): JSX.Element => {
  const { brain } = useBrainFetcher({
    brainId,
  });

  if (brain?.brain_type === "api") {
    return <ApiBrainSecretsInputs brainId={brainId} />;
  }

  return <AddedKnowledge brainId={brainId} />;
};
