import { Fragment } from "react";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

export const SelectedBrainTag = (): JSX.Element => {
  const { currentBrain } = useBrainContext();
  if (currentBrain === undefined) {
    return <Fragment />;
  }

  return (
    <div className="mb-4 flex items-center justify-center w-full">
      <div className="px-3 py-1 w-content bg-accent-hover rounded-full flex items-center justify-center text-white">
        #{currentBrain.name}
      </div>
    </div>
  );
};
