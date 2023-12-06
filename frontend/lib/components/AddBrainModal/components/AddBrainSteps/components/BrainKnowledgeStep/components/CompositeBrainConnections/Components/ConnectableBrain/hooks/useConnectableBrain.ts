import { CheckedState } from "@radix-ui/react-checkbox";
import { UUID } from "crypto";
import { useFormContext } from "react-hook-form";

import { CreateBrainProps } from "@/lib/components/AddBrainModal/types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useConnectableBrain = () => {
  const { setValue, getValues } = useFormContext<CreateBrainProps>();

  const onCheckedChange = ({
    checked,
    brainId,
  }: {
    checked: CheckedState;
    brainId: UUID;
  }) => {
    if (checked === "indeterminate") {
      return;
    }
    const connected_brains_ids = getValues("connected_brains_ids") ?? [];
    if (checked) {
      setValue("connected_brains_ids", [...connected_brains_ids, brainId]);
    } else {
      setValue(
        "connected_brains_ids",
        connected_brains_ids.filter((id) => id !== brainId)
      );
    }
  };

  return {
    onCheckedChange,
  };
};
