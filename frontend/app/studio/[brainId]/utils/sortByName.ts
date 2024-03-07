import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

export const sortBrainsByName = (
  minimalBrains: MinimalBrainForUser[]
): MinimalBrainForUser[] => {
  // Use the sort method to sort the array by the 'name' property
  const sortedMinimalBrains = minimalBrains
    .slice()
    .sort((a, b) => a.name.localeCompare(b.name));

  return sortedMinimalBrains;
};
