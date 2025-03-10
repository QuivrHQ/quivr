"use client";

import { FormEvent, useState } from "react";

import { useUserApi } from "@/lib/api/user/useUserApi";
import { ResetPasswordRequest } from "@/lib/api/user/user";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useSupabase } from "@/lib/context/SupabaseProvider";

import styles from "./ResetPassword.module.scss";

interface ResetPasswordProps {
  onClose: () => void;
}

export const ResetPassword = ({ onClose }: ResetPasswordProps): JSX.Element => {
  // const { t } = useTranslation(["translation", "user", "logout"]);
  const { resetPassword } = useUserApi();
  const { supabase } = useSupabase();

  // Reset password state
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [isResettingPassword, setIsResettingPassword] = useState(false);
  const [resetSuccess, setResetSuccess] = useState(false);

  const handleSubmit = async (e: FormEvent): Promise<void> => {
    e.preventDefault();
    setPasswordError("");

    // Validate passwords
    if (newPassword.length < 6) {
      setPasswordError("New password must be at least 6 characters long");

      return;
    }

    if (newPassword !== confirmPassword) {
      setPasswordError("New password and confirmation do not match");

      return;
    }

    try {
      setIsResettingPassword(true);

      const passwordData: ResetPasswordRequest = {
        current_password: currentPassword,
        new_password: newPassword,
        confirm_password: confirmPassword,
      };

      await resetPassword(passwordData);

      // Refresh the session after password change
      await supabase.auth.refreshSession();

      setResetSuccess(true);
    } catch (error) {
      if (error instanceof Error) {
        setPasswordError(error.message);
      } else {
        setPasswordError("An error occurred while resetting your password");
      }
    } finally {
      setIsResettingPassword(false);
    }
  };

  return (
    <div className={styles.reset_password_container}>
      <h2>Reset Your Password</h2>

      {resetSuccess ? (
        <div className={styles.success_message}>
          <p>Your password has been successfully updated!</p>
          <QuivrButton
            onClick={() => {
              onClose();
              setResetSuccess(false);
              setCurrentPassword("");
              setNewPassword("");
              setConfirmPassword("");
            }}
            color='primary'
            label='Close'
            iconName='close'
          />
        </div>
      ) : (
        <form
          onSubmit={(e) => void handleSubmit(e)}
          className={styles.reset_password_form}
        >
          <div className={styles.form_group}>
            <label htmlFor='current_password'>Current password</label>
            <input
              id='current_password'
              type='password'
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              placeholder='Enter your current password'
              required
            />
          </div>

          <div className={styles.form_group}>
            <label htmlFor='new_password'>Create a password</label>
            <input
              id='new_password'
              type='password'
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder='Enter your new password'
              required
            />
          </div>

          <div className={styles.form_group}>
            <label htmlFor='confirm_password'>Confirm your password</label>
            <input
              id='confirm_password'
              type='password'
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder='Confirm your new password'
              required
            />
          </div>

          {passwordError && (
            <div className={styles.error_message}>{passwordError}</div>
          )}

          <div className={styles.buttons}>
            <QuivrButton
              onClick={onClose}
              color='primary'
              label='Cancel'
              iconName='close'
            />
            <button type='submit'>
              <QuivrButton
                isLoading={isResettingPassword}
                color='primary'
                label='Save'
                iconName='check'
              />
            </button>
          </div>
        </form>
      )}
    </div>
  );
};

export default ResetPassword;
