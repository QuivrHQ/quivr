import { UUID } from "crypto";
import { MdDelete } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

export const DeleteBrain = ({ brainId }: { brainId: UUID }): JSX.Element => {
  const { deleteBrain } = useBrainContext();

  return (
    <Button
      className="group-hover:visible invisible hover:text-red-500 transition-[colors,opacity] p-1"
      onClick={() => void deleteBrain(brainId)}
      variant={"tertiary"}
    >
      <MdDelete className="text-xl" />
    </Button>
  );
};
