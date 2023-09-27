import { UUID } from "crypto";

const brainDataKey = "quivr-knowledge";

export const getKnowledgeDataKey = (knowledgeId: UUID): string =>
  `${brainDataKey}-${knowledgeId}`;
