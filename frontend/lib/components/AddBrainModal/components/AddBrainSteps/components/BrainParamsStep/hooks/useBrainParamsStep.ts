import { useFormContext } from "react-hook-form";

import { CreateBrainProps } from "@/lib/components/AddBrainModal/types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainParamsStep = () => {
  const { watch } = useFormContext<CreateBrainProps>();
  const brainName = watch("name");
  const description = watch("description");

  const isNextButtonDisabled = brainName === "" || description === "";

  return {
    isNextButtonDisabled,
  };
};
