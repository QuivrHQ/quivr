import { FormProvider, useForm } from "react-hook-form";

import { addBrainDefaultValues } from "@/lib/config/defaultBrainConfig";

import { AddBrainConfig } from "./components/AddBrainConfig/AddBrainConfig";
import { CreateBrainProps } from "./components/AddBrainConfig/types";

type AddBrainModalProps = {
  triggerClassName?: string;
};

export const AddBrainModal = ({
  triggerClassName,
}: AddBrainModalProps): JSX.Element => {
  const defaultValues: CreateBrainProps = {
    ...addBrainDefaultValues,
    prompt: {
      title: "",
      content: "",
    },
    setDefault: true,
  };

  const methods = useForm<CreateBrainProps>({
    defaultValues,
  });

  return (
    <FormProvider {...methods}>
      <AddBrainConfig triggerClassName={triggerClassName} />
    </FormProvider>
  );
};
