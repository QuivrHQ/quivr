import { useState } from 'react';
import { FormProvider, useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';

import { useUserApi } from '@/lib/api/user/useUserApi';
import { Modal } from '@/lib/components/ui/Modal/Modal';
import {
  MultiSelect,
  SelectOptionProps,
} from '@/lib/components/ui/MultiSelect/MultiSelect';
import { useBrainContext } from '@/lib/context/BrainProvider/hooks/useBrainContext';
import { useSupabase } from '@/lib/context/SupabaseProvider';

import styles from './CreateUserModal.module.scss';

import Button from '../ui/Button';
import { TextInput } from '../ui/TextInput/TextInput';

type CreateUserProps = {
  firstName: string;
  lastName: string;
  email: string;
  brains: string[];
};

type CreateUserModalProps = {
  isOpen: boolean;
  setOpen: (isOpen: boolean) => void;
};

export const CreateUserModal = ({
  isOpen,
  setOpen,
}: CreateUserModalProps): JSX.Element => {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const { t } = useTranslation(['translation']);
  const { allBrains } = useBrainContext();
  const { supabase } = useSupabase();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { createUser } = useUserApi();

  const brainOptions: SelectOptionProps<string>[] = allBrains.map((brain) => ({
    label: brain.name,
    value: brain.id,
  }));

  const [selectedBrains, setSelectedBrains] = useState<
    SelectOptionProps<string>[]
  >([]);

  const methods = useForm<CreateUserProps>({
    defaultValues: {
      firstName: '',
      lastName: '',
      email: '',
      brains: [],
    },
    mode: 'onChange',
  });

  const { register, handleSubmit, formState, setValue, watch, reset } = methods;
  const { errors } = formState;
  
  // Watch form values
  const firstName = watch('firstName');
  const lastName = watch('lastName');
  const email = watch('email');

  const onSubmit = async (data: CreateUserProps): Promise<void> => {
    try {
      setIsSubmitting(true);
      setError(null);

      // Add the selected brains to the form data
      data.brains = selectedBrains.map((brain) => brain.value);

      // Call the backend API to create the user
      await createUser(data);

      console.log('User created successfully');
      setOpen(false);

      // Reset form
      reset();
      setSelectedBrains([]);
    } catch (error) {
      console.error('Error creating user:', error);
      setError(
        error instanceof Error ? error.message : 'Failed to create user'
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

  const handleInputChange = (field: keyof CreateUserProps, value: string): void => {
    setValue(field, value, { shouldValidate: true });
  };

  return (
    <FormProvider {...methods}>
      <Modal
        title='New user'
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
              Cancel
            </Button>
            <Button
              type='submit'
              variant='primary'
              isLoading={isSubmitting}
              onClick={handleSubmit(onSubmit)}
            >
              Create
            </Button>
          </div>
        }
      >
        <div className={styles.create_user_form}>
          {error && <div className={styles.error_message}>{error}</div>}
          <div className={styles.form_fields}>
            <div className={styles.form_field}>
              <label htmlFor='firstName'>First name</label>
              <TextInput
                label='First name'
                inputValue={firstName}
                setInputValue={(value) => handleInputChange('firstName', value)}
                {...register('firstName', {
                  required: 'First name is required',
                })}
              />
              {errors.firstName && (
                <span className={styles.error}>
                  {errors.firstName.message}
                </span>
              )}
            </div>

            <div className={styles.form_field}>
              <label htmlFor='lastName'>Last name</label>
              <TextInput
                label='Last name'
                inputValue={lastName}
                setInputValue={(value) => handleInputChange('lastName', value)}
                {...register('lastName', {
                  required: 'Last name is required',
                })}
              />
              {errors.lastName && (
                <span className={styles.error}>
                  {errors.lastName.message}
                </span>
              )}
            </div>

            <div className={styles.form_field}>
              <label htmlFor='email'>Email</label>
              <TextInput
                label='Email'
                inputValue={email}
                setInputValue={(value) => handleInputChange('email', value)}
                {...register('email', {
                  required: 'Email is required',
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: 'Invalid email address',
                  },
                })}
              />
              {errors.email && (
                <span className={styles.error}>
                  {errors.email.message}
                </span>
              )}
            </div>

            <div className={styles.form_field}>
              <label htmlFor='brains'>Brains</label>
              <MultiSelect
                options={brainOptions}
                selectedOptions={selectedBrains}
                onChange={handleBrainsChange}
                placeholder='Select brains'
                iconName='brain'
              />
            </div>
          </div>
        </div>
      </Modal>
    </FormProvider>
  );
};
