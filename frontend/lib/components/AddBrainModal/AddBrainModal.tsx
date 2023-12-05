import { FormProvider, useForm } from "react-hook-form";

import { addBrainDefaultValues } from "@/lib/config/defaultBrainConfig";
import { KnowledgeToFeedProvider } from "@/lib/context";

import { AddBrainSteps } from "./components/AddBrainSteps/AddBrainSteps";
import { CreateBrainProps } from "./types";

type AddBrainModalProps = {
  triggerClassName?: string;
};

export const AddBrainModal = ({
  triggerClassName,
}: AddBrainModalProps): JSX.Element => {
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
      <KnowledgeToFeedProvider>
        <AddBrainSteps triggerClassName={triggerClassName} />
      </KnowledgeToFeedProvider>
    </FormProvider>
  );
};
