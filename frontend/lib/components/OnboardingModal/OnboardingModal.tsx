import { Controller, FormProvider, useForm } from "react-hook-form";

import { Modal } from "@/lib/components/ui/Modal/Modal";
import { useOnboardingContext } from "@/lib/context/OnboardingProvider/hooks/useOnboardingContext";

import styles from "./OnboardingModal.module.scss";

import { OnboardingProps } from "../OnboardingModal/types/types";
import { FieldHeader } from "../ui/FieldHeader/FieldHeader";
import { TextInput } from "../ui/TextInput/TextInput";

export const OnboardingModal = (): JSX.Element => {
  const { isOnboardingModalOpened, setIsOnboardingModalOpened } =
    useOnboardingContext();

  const methods = useForm<OnboardingProps>({});

  return (
    <FormProvider {...methods}>
      <Modal
        title="Welcome to Quivr!"
        desc="Let us know a bit more about you to get started."
        bigModal={true}
        isOpen={isOnboardingModalOpened}
        setOpen={setIsOnboardingModalOpened}
        CloseTrigger={<div />}
      >
        <div className={styles.form_wrapper}>
          <div>
            <FieldHeader iconName="user" label="Username" mandatory={true} />
            <Controller
              name="username"
              render={({ field }) => (
                <TextInput
                  label="Choose a username"
                  inputValue={field.value as string}
                  setInputValue={field.onChange}
                />
              )}
            />
          </div>
          <div>
            <FieldHeader iconName="user" label="Company" />
            <Controller
              name="companyName"
              render={({ field }) => (
                <TextInput
                  label="Company Name"
                  inputValue={field.value as string}
                  setInputValue={field.onChange}
                />
              )}
            />
          </div>
        </div>
      </Modal>
    </FormProvider>
  );
};
