const BRAIN_DATA_KEY = "quivr-brains";

export const getBrainDataKey = (brainId: string): string =>
  `${BRAIN_DATA_KEY}-${brainId}`;

export const getBrainKnowledgeDataKey = (brainId: string): string =>
  `${BRAIN_DATA_KEY}-${brainId}-knowledge`;

export const PUBLIC_BRAINS_KEY = "quivr-public-brains";
