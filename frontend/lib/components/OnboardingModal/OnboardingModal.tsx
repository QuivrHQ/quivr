import { FormProvider, useForm } from "react-hook-form";

import { Modal } from "@/lib/components/ui/Modal/Modal";
import { addBrainDefaultValues } from "@/lib/config/defaultBrainConfig";

import { CreateBrainProps } from "../AddBrainModal/types/types";

export const AddBrainModal = (): JSX.Element => {
  const defaultValues: CreateBrainProps = {
    ...addBrainDefaultValues,
    setDefault: true,
    brainCreationStep: "BRAIN_TYPE",
  };

  const methods = useForm<CreateBrainProps>({
    defaultValues,
  });

  return (
    <FormProvider {...methods}>
      <Modal
        title="Title"
        desc="Desc"
        bigModal={true}
        CloseTrigger={<div />}
      ></Modal>
    </FormProvider>
  );
};
