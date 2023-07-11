import { UUID } from "crypto";
import { MdDelete } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { ShareBrain } from "./ShareBrain";

type BrainActionsProps = {
  brainId: UUID;
};

export const BrainActions = ({ brainId }: BrainActionsProps): JSX.Element => {
  const { deleteBrain } = useBrainContext();

  return (
    <div className="absolute right-0 flex flex-row">
      <ShareBrain brainId={brainId} />
      <Button
        className="group-hover:visible invisible hover:text-red-500 transition-[colors,opacity] p-1"
        onClick={() => void deleteBrain(brainId)}
        variant={"tertiary"}
      >
        <MdDelete className="text-xl" />
      </Button>
    </div>
  );
};
