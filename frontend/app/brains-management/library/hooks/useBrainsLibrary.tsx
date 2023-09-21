import { useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";

import { PUBLIC_BRAINS_KEY } from "@/lib/api/brain/config";
import { useBrainApi } from "@/lib/api/brain/useBrainApi";
import { PublicBrain } from "@/lib/context/BrainProvider/types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainsLibrary = () => {
  const [searchBarText, setSearchBarText] = useState("");
  const { getPublicBrains } = useBrainApi();
  const { data: publicBrains = [] } = useQuery({
    queryKey: [PUBLIC_BRAINS_KEY],
    queryFn: getPublicBrains,
  });

  const [displayingPublicBrains, setDisplayingPublicBrains] = useState<
    PublicBrain[]
  >([]);

  useEffect(() => {
    setDisplayingPublicBrains(publicBrains);
  }, [publicBrains]);

  useEffect(() => {
    if (searchBarText === "") {
      setDisplayingPublicBrains(publicBrains);

      return;
    }
    setDisplayingPublicBrains(
      publicBrains.filter((brain) =>
        brain.name.toLowerCase().includes(searchBarText.toLowerCase())
      )
    );
  }, [publicBrains, searchBarText]);

  return {
    displayingPublicBrains,
    searchBarText,
    setSearchBarText,
  };
};
