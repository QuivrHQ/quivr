"use client";

import { FormEvent, useState } from "react";
import { useTranslation } from "react-i18next";

import { useUserApi } from "@/lib/api/user/useUserApi";
import { ResetPasswordRequest } from "@/lib/api/user/user";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";

import styles from "./ResetPassword.module.scss";

interface ResetPasswordProps {
  onClose: () => void;
}

export const ResetPassword = ({ onClose }: ResetPasswordProps): JSX.Element => {
  const { t } = useTranslation(["translation", "user", "logout"]);
  const { resetPassword } = useUserApi();

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
      setPasswordError(t("new_pass_least_6", { ns: "user" }));

      return;
    }

    if (newPassword !== confirmPassword) {
      setPasswordError(t("new_pass_confirmed", { ns: "user" }));

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

      setResetSuccess(true);
    } catch (error) {
      if (error instanceof Error) {
        setPasswordError(error.message);
      } else {
        setPasswordError(t("an_error_occurred", { ns: "user" }));
      }
    } finally {
      setIsResettingPassword(false);
    }
  };

  return (
    <div className={styles.reset_password_container}>
      <h2>{t("reset_password", { ns: "user" })}</h2>

      {resetSuccess ? (
        <div className={styles.success_message}>
          <p>{t("reset_password_success", { ns: "user" })}</p>
          <QuivrButton
            onClick={() => {
              onClose();
              setResetSuccess(false);
              setCurrentPassword("");
              setNewPassword("");
              setConfirmPassword("");
            }}
            color='primary'
            label={t("close", { ns: "user" })}
            iconName='close'
          />
        </div>
      ) : (
        <form
          onSubmit={(e) => void handleSubmit(e)}
          className={styles.reset_password_form}
        >
          <div className={styles.form_group}>
            <label htmlFor='current_password'>{t("current_password", { ns: "user" })}</label>
            <input
              id='current_password'
              type='password'
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              placeholder={t("current_password_plc", { ns: "user" })}
              required
            />
          </div>

          <div className={styles.form_group}>
            <label htmlFor='new_password'>{t("new_password", { ns: "user" })}</label>
            <input
              id='new_password'
              type='password'
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder={t("new_password_plc", { ns: "user" })}
              required
            />
          </div>

          <div className={styles.form_group}>
            <label htmlFor='confirm_password'>{t("confirm_password", { ns: "user" })}</label>
            <input
              id='confirm_password'
              type='password'
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder={t("confirm_password_plc", { ns: "user" })}
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
              label={t("cancel", { ns: "user" })}
              iconName='close'
            />
            <button type='submit'>
              <QuivrButton
                isLoading={isResettingPassword}
                color='primary'
                label={t("save", { ns: "user" })}
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
