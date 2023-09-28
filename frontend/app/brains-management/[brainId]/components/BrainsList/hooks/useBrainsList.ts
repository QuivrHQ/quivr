import { UUID } from "crypto";
import { redirect, useParams, usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { sortBrainsByName } from "../../../utils/sortByName";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainsList = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const { allBrains } = useBrainContext();
  const { currentBrainId } = useBrainContext();
  const params = useParams();

  const brainId = params?.brainId as UUID | undefined;

  const pathname = usePathname();

  const isOnBrainsLibraryPage = pathname?.includes("/library") ?? false;

  const brains = allBrains.filter((brain) => {
    const query = searchQuery.toLowerCase();
    const name = brain.name.toLowerCase();

    return name.includes(query);
  });

  useEffect(() => {
    if (brainId !== undefined) {
      return;
    }

    if (
      currentBrainId !== null &&
      pathname !== null &&
      !isOnBrainsLibraryPage
    ) {
      redirect(`/brains-management/${currentBrainId}`);
    }
  }, [brainId, currentBrainId, pathname, isOnBrainsLibraryPage]);

  return {
    searchQuery,
    setSearchQuery,
    brains: sortBrainsByName(brains),
    isOnBrainsLibraryPage,
  };
};
