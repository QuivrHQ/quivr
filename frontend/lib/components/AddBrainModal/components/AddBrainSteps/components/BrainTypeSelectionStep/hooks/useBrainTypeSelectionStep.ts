import { useEffect } from "react";
import { useFormContext } from "react-hook-form";

import { CreateBrainProps } from "@/lib/components/AddBrainModal/types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainTypeSelectionStep = () => {
  const { register, watch, reset, setValue } =
    useFormContext<CreateBrainProps>();
  const brainType = watch("brain_type");

  useEffect(() => {
    const currentBrainType = brainType;
    reset();
    setValue("brain_type", currentBrainType);
  }, [brainType, reset, setValue]);

  return {
    register,
  };
};
