import { useEffect, useState } from "react";
import { FormProvider, useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import { useUserApi } from "@/lib/api/user/useUserApi";
import { UserIdentity } from "@/lib/api/user/user";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import {
  MultiSelect,
  SelectOptionProps,
} from "@/lib/components/ui/MultiSelect/MultiSelect";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import styles from "./CreateUserModal.module.scss";

import Button from "../ui/Button";
import { TextInput } from "../ui/TextInput/TextInput";

type UserFormProps = {
  firstName: string;
  lastName: string;
  email: string;
  brains: string[];
  id?: string;
};

type CreateUserModalProps = {
  isOpen: boolean;
  setOpen: (isOpen: boolean) => void;
  isEditMode?: boolean;
  userData?: UserIdentity;
  onSuccess?: () => void;
};

export const CreateUserModal = ({
  isOpen,
  setOpen,
  isEditMode = false,
  userData,
  onSuccess,
}: CreateUserModalProps): JSX.Element => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { t } = useTranslation(["user"]);
  const { allBrains } = useBrainContext();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { createUser, updateUser } = useUserApi();

  const brainOptions: SelectOptionProps<string>[] = allBrains.map((brain) => ({
    label: brain.name,
    value: brain.id,
  }));

  const [selectedBrains, setSelectedBrains] = useState<
    SelectOptionProps<string>[]
  >([]);

  const methods = useForm<UserFormProps>({
    defaultValues: {
      firstName: "",
      lastName: "",
      email: "",
      brains: [],
      id: "",
    },
    mode: "onChange",
  });

  const { register, handleSubmit, formState, setValue, watch, reset } = methods;
  const { errors } = formState;

  // Watch form values
  const firstName = watch("firstName");
  const lastName = watch("lastName");
  const email = watch("email");

  // Effect to populate form when in edit mode
  useEffect(() => {
    if (isEditMode && userData) {
      // Extract first and last name from username
      const nameParts = userData.username.split(" ");
      // eslint-disable-next-line @typescript-eslint/no-shadow
      const firstName = nameParts[0] ?? "";
      // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition, @typescript-eslint/no-shadow
      const lastName = nameParts.slice(1).join(" ") ?? "";

      // Set form values
      setValue("firstName", firstName);
      setValue("lastName", lastName);
      setValue("email", userData.email ?? "");
      setValue("id", userData.id);

      // Set selected brains
      if (userData.brains && userData.brain_names) {
        const userBrainOptions = userData.brains.map((brainId, index) => ({
          value: brainId,
          label: userData.brain_names?.[index] ?? brainId,
        }));
        setSelectedBrains(userBrainOptions);
      }
    }
  }, [isEditMode, userData, setValue]);

  const onSubmit = async (data: UserFormProps): Promise<void> => {
    try {
      setIsSubmitting(true);
      setError(null);

      // Add the selected brains to the form data
      data.brains = selectedBrains.map((brain) => brain.value);

      if (isEditMode && userData) {
        // Call the backend API to update the user
        await updateUser({
          ...data,
          id: userData.id,
        });
        console.log("User updated successfully");
      } else {
        // Call the backend API to create the user
        await createUser(data);
        console.log("User created successfully");
      }

      setOpen(false);

      // Call onSuccess callback if provided
      if (onSuccess) {
        onSuccess();
      }

      // Reset form if not in edit mode
      if (!isEditMode) {
        reset();
        setSelectedBrains([]);
      }
      // eslint-disable-next-line @typescript-eslint/no-shadow
    } catch (error) {
      console.error(
        `Error ${isEditMode ? "updating" : "creating"} user:`,
        error
      );
      setError(
        error instanceof Error
          ? error.message
          : `Failed to ${isEditMode ? "update" : "create"} user`
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleBrainsChange = (selectedBrainIds: string[]): void => {
    const newSelectedBrains = brainOptions.filter((option) =>
      selectedBrainIds.includes(option.value)
    );
    setSelectedBrains(newSelectedBrains);
  };

  const handleInputChange = (
    field: keyof UserFormProps,
    value: string
  ): void => {
    setValue(field, value, { shouldValidate: true });
  };

  return (
    <FormProvider {...methods}>
      <Modal
        title={isEditMode ? t("edit_user", { ns: "user" }) : t("create_user", { ns: "user" })}
        isOpen={isOpen}
        setOpen={setOpen}
        size='normal'
        CloseTrigger={
          <div className={styles.actions}>
            <Button
              type='button'
              variant='secondary'
              onClick={() => setOpen(false)}
            >
              {t("cancel", { ns: "user" })}
            </Button>
            <Button
              type='submit'
              variant='primary'
              isLoading={isSubmitting}
              // eslint-disable-next-line @typescript-eslint/no-misused-promises
              onClick={handleSubmit(onSubmit)}
            >
              {isEditMode ? t("save_changes", { ns: "user" }) : t("create", { ns: "user" })}
            </Button>
          </div>
        }
      >
        <div className={styles.create_user_form}>
          {error && <div className={styles.error_message}>{error}</div>}
          <div className={styles.form_fields}>
            <div className={styles.form_field}>
              <label htmlFor='firstName'>{t("first_name", { ns: "user" })}</label>
              <TextInput
                label={t("first_name", { ns: "user" })}
                inputValue={firstName}
                setInputValue={(value) => handleInputChange("firstName", value)}
                {...register("firstName", {
                  required: t("first_name_required", { ns: "user" }),
                })}
              />
              {errors.firstName && (
                <span className={styles.error}>{errors.firstName.message}</span>
              )}
            </div>

            <div className={styles.form_field}>
              <label htmlFor='lastName'>{t("last_name", { ns: "user" })}</label>
              <TextInput
                label={t("last_name", { ns: "user" })}
                inputValue={lastName}
                setInputValue={(value) => handleInputChange("lastName", value)}
                {...register("lastName", {
                  required: t("last_name_required", { ns: "user" }),
                })}
              />
              {errors.lastName && (
                <span className={styles.error}>{errors.lastName.message}</span>
              )}
            </div>

            <div className={styles.form_field}>
              <label htmlFor='email'>{t("email", { ns: "user" })}</label>
              <TextInput
                label={t("email", { ns: "user" })}
                inputValue={email}
                setInputValue={(value) => handleInputChange("email", value)}
                disabled={isEditMode}
                {...register("email", {
                  required: t("email_required", { ns: "user" }),
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: t("email_invalid", { ns: "user" }),
                  },
                })}
              />
              {errors.email && (
                <span className={styles.error}>{errors.email.message}</span>
              )}
            </div>

            <div className={styles.form_field}>
              <label htmlFor='brains'>{t("brains", { ns: "user" })}</label>
              <MultiSelect
                options={brainOptions}
                selectedOptions={selectedBrains}
                onChange={handleBrainsChange}
                placeholder={t("select_brains", { ns: "user" })}
                iconName='brain'
              />
            </div>
          </div>
        </div>
      </Modal>
    </FormProvider>
  );
};
