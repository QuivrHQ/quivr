import { FormProvider, useForm } from "react-hook-form";

import { Modal } from "@/lib/components/ui/Modal/Modal";
import { useOnboardingContext } from "@/lib/context/OnboardingProvider/hooks/useOnboardingContext";

import { OnboardingProps } from "../OnboardingModal/types/types";

export const OnboardingModal = (): JSX.Element => {
  const { isOnboardingModalOpened, setIsOnboardingModalOpened } =
    useOnboardingContext();

  const methods = useForm<OnboardingProps>({});

  return (
    <FormProvider {...methods}>
      <Modal
        title="Title"
        desc="Desc"
        bigModal={true}
        isOpen={isOnboardingModalOpened}
        setOpen={setIsOnboardingModalOpened}
        CloseTrigger={<div />}
      >
        HEY
      </Modal>
    </FormProvider>
  );
};
