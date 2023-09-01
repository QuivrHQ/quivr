const brainDataKey = "quivr-brains";

export const getBrainDataKey = (brainId: string): string =>
  `${brainDataKey}-${brainId}`;
