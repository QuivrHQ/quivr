import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

import { DeleteBrain, ShareBrain } from "./components";
import { BrainRoleType } from "./types";

type BrainActionsProps = {
  brain: MinimalBrainForUser;
};

const requiredAccessToShareBrain: BrainRoleType[] = ["Owner", "Editor"];

export const BrainActions = ({ brain }: BrainActionsProps): JSX.Element => {
  return (
    <div className="absolute right-0 flex flex-row">
      {requiredAccessToShareBrain.includes(brain.role) && (
        <ShareBrain brainId={brain.id} name={brain.name} />
      )}
      <DeleteBrain brainId={brain.id} />
    </div>
  );
};
