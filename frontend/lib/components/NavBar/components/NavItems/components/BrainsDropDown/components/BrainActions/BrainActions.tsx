import { UUID } from "crypto";

import { DeleteBrain, ShareBrain } from "./components";

type BrainActionsProps = {
  brainId: UUID;
};

export const BrainActions = ({ brainId }: BrainActionsProps): JSX.Element => {
  return (
    <div className="absolute right-0 flex flex-row">
      <ShareBrain brainId={brainId} />
      <DeleteBrain brainId={brainId} />
    </div>
  );
};
