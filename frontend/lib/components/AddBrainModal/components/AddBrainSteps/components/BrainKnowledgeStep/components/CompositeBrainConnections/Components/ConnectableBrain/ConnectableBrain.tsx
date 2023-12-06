import { Checkbox } from "@/lib/components/ui/Checkbox";
import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

import { useConnectableBrain } from "./hooks/useConnectableBrain";

type ConnectableBrainProps = {
  brain: MinimalBrainForUser;
};

export const ConnectableBrain = ({
  brain,
}: ConnectableBrainProps): JSX.Element => {
  const { onCheckedChange } = useConnectableBrain();

  return (
    <div className="flex flex-row items-center gap-2">
      <Checkbox
        className="text-white"
        onCheckedChange={(checked) =>
          onCheckedChange({
            brainId: brain.id,
            checked,
          })
        }
        id={`connected_brains_ids-${brain.id}`}
      />
      <label
        htmlFor={`connected_brains_ids-${brain.id}`}
        className="text-md font-medium leading-none cursor-pointer"
      >
        {brain.name}
      </label>
    </div>
  );
};
