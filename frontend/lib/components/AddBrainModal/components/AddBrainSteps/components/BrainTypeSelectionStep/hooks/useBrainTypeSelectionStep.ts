import { useFormContext } from "react-hook-form";

import { CreateBrainProps } from "@/lib/components/AddBrainModal/types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainTypeSelectionStep = () => {
  const { register } = useFormContext<CreateBrainProps>();

  return {
    register,
  };
};
