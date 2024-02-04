import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

import { BrainItem } from "./BrainItem";

type BrainsListProps = {
  brains: MinimalBrainForUser[];
};

export const BrainsList = ({ brains }: BrainsListProps): JSX.Element => {
  return (
    <div className="flex flex-1 flex-col items-center justify-center">
      <div className="w-full lg:grid-cols-4 md:grid-cols-3 grid mt-5 gap-3 items-stretch">
        {brains.map((brain) => (
          <div key={brain.id} className="h-[180px]">
            <BrainItem brain={brain} />
          </div>
        ))}
      </div>
    </div>
  );
};
