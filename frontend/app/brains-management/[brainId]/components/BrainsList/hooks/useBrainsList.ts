import { UUID } from "crypto";
import { redirect, useParams, usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useDevice } from "@/lib/hooks/useDevice";

import { sortBrainsByName } from "../../../utils/sortByName";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainsList = () => {
  const { isMobile } = useDevice();
  const [opened, setOpened] = useState(!isMobile);
  const [searchQuery, setSearchQuery] = useState("");
  const { allBrains } = useBrainContext();
  const { currentBrainId } = useBrainContext();
  const params = useParams();

  const brainId = params?.brainId as UUID | undefined;

  const pathname = usePathname();

  const isOnBrainsLibraryPage = pathname?.includes("/library") ?? false;

  useEffect(() => {
    setOpened(!isMobile);
  }, [isMobile, pathname]);

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
    opened,
    setOpened,
    searchQuery,
    setSearchQuery,
    brains: sortBrainsByName(brains),
    isOnBrainsLibraryPage,
  };
};
