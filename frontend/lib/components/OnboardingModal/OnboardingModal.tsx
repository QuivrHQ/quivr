import { Controller, FormProvider, useForm } from "react-hook-form";

import { useUserApi } from "@/lib/api/user/useUserApi";
import { CompanyRole, CompanySize } from "@/lib/api/user/user";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import { useOnboardingContext } from "@/lib/context/OnboardingProvider/hooks/useOnboardingContext";

import styles from "./OnboardingModal.module.scss";

import { OnboardingProps } from "../OnboardingModal/types/types";
import { FieldHeader } from "../ui/FieldHeader/FieldHeader";
import { QuivrButton } from "../ui/QuivrButton/QuivrButton";
import { SingleSelector } from "../ui/SingleSelector/SingleSelector";
import { TextInput } from "../ui/TextInput/TextInput";

export const OnboardingModal = (): JSX.Element => {
  const { isOnboardingModalOpened, setIsOnboardingModalOpened } =
    useOnboardingContext();

  const methods = useForm<OnboardingProps>({
    defaultValues: {
      username: "",
      companyName: "",
      companySize: undefined,
      roleInCompany: "",
    },
  });
  const { watch } = methods;
  const username = watch("username");

  const { updateUserIdentity } = useUserApi();

  const companySizeOptions = Object.entries(CompanySize).map(([, value]) => ({
    label: value,
    value: value,
  }));

  const companyRoleOptions = Object.entries(CompanyRole).map(([, value]) => ({
    label: value,
    value: value,
  }));

  const submitForm = async () => {
    await updateUserIdentity({
      username: methods.getValues("username"),
      company: methods.getValues("companyName"),
      onboarded: true,
      company_size: methods.getValues("companySize"),
      role_in_company: methods.getValues("roleInCompany") as
        | CompanyRole
        | undefined,
    });
    window.location.reload();
  };

  return (
    <FormProvider {...methods}>
      <Modal
        title="Welcome to Quivr!"
        desc="Let us know a bit more about you to get started."
        isOpen={isOnboardingModalOpened}
        setOpen={setIsOnboardingModalOpened}
        CloseTrigger={<div />}
        unclosable={true}
      >
        <div className={styles.modal_content_wrapper}>
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
              <FieldHeader iconName="office" label="Company" />
              <Controller
                name="companyName"
                render={({ field }) => (
                  <TextInput
                    label="Your company name"
                    inputValue={field.value as string}
                    setInputValue={field.onChange}
                  />
                )}
              />
            </div>
            <div>
              <FieldHeader iconName="chair" label="Role" />
              <Controller
                name="roleInCompany"
                render={({ field }) => (
                  <SingleSelector
                    iconName="radio"
                    options={companyRoleOptions}
                    placeholder="What is your role in the company?"
                    selectedOption={
                      field.value
                        ? {
                            label: field.value as string,
                            value: field.value as string,
                          }
                        : undefined
                    }
                    onChange={field.onChange}
                  />
                )}
              />
            </div>
            <div>
              <FieldHeader iconName="hashtag" label="Size of your company" />
              <Controller
                name="companySize"
                render={({ field }) => (
                  <SingleSelector
                    iconName="radio"
                    options={companySizeOptions}
                    placeholder="Number of employees in your company"
                    selectedOption={
                      field.value
                        ? {
                            label: field.value as string,
                            value: field.value as string,
                          }
                        : undefined
                    }
                    onChange={field.onChange}
                  />
                )}
              />
            </div>
          </div>
          <div className={styles.button_wrapper}>
            <QuivrButton
              iconName="chevronRight"
              label="Submit"
              color="primary"
              onClick={() => submitForm()}
              disabled={!username}
            />
          </div>
        </div>
      </Modal>
    </FormProvider>
  );
};
