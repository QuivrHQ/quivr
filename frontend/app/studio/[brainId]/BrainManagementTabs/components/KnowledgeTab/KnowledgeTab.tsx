"use client";
import { UUID } from "crypto";

import { AddedKnowledge } from "./components/AddedKnowledge/AddedKnowledge";

type KnowledgeTabProps = {
  brainId: UUID;
  hasEditRights: boolean;
};
export const KnowledgeTab = ({ brainId }: KnowledgeTabProps): JSX.Element => {
  return <AddedKnowledge brainId={brainId} />;
};
