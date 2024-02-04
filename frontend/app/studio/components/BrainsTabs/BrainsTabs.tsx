import Spinner from "@/lib/components/ui/Spinner";

import { BrainSearchBar } from "./components/BrainSearchBar";
import { BrainsList } from "./components/BrainsList";
import { useBrainsTabs } from "./hooks/useBrainsTabs";

export const BrainsTabs = (): JSX.Element => {
  const { searchQuery, isFetchingBrains, setSearchQuery, brains } =
    useBrainsTabs();

  if (isFetchingBrains && brains.length === 0) {
    return (
      <div className="flex w-full h-full justify-center items-center">
        <Spinner />
      </div>
    );
  }

  return (
    <div>
      <BrainSearchBar
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
      />

      <BrainsList brains={brains} />
    </div>
  );
};
