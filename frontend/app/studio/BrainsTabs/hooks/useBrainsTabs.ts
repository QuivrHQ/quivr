import { useState } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainsTabs = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const { allBrains, isFetchingBrains } = useBrainContext();

  const brains = allBrains.filter((brain) => {
    const query = searchQuery.toLowerCase();
    const name = brain.name.toLowerCase();

    return name.includes(query);
  });

  const privateBrains = brains.filter((brain) => brain.status === "private");

  const publicBrains = brains.filter((brain) => brain.status === "public");

  return {
    searchQuery,
    setSearchQuery,
    brains,
    privateBrains,
    publicBrains,
    isFetchingBrains,
  };
};
