const brainDataKey = "quivr-brains";

export const getBrainDataKey = (brainId: string): string =>
  `${brainDataKey}-${brainId}`;

export const getBrainKnowledgeDataKey = (brainId: string): string =>
  `${brainDataKey}-${brainId}-knowledge`;
