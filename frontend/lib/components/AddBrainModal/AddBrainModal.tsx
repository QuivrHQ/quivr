import { FormProvider, useForm } from "react-hook-form";

import { defaultBrainConfig } from "@/lib/config/defaultBrainConfig";
import { BrainConfig } from "@/lib/types/brainConfig";

import { AddBrainConfig } from "./components/AddBrainConfig/AddBrainConfig";

type AddBrainModalProps = {
  triggerClassName?: string;
};

export const AddBrainModal = ({
  triggerClassName,
}: AddBrainModalProps): JSX.Element => {
  const methods = useForm<BrainConfig>({
    defaultValues: defaultBrainConfig,
  });

  return (
    <FormProvider {...methods}>
      <AddBrainConfig triggerClassName={triggerClassName} />
    </FormProvider>
  );
};
