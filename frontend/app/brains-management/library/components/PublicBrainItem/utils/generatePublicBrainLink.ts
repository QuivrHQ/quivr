export const generatePublicBrainLink = (brainId: string): string =>
  `${window.location.origin}/brains-management/library?brainId=${brainId}`;
