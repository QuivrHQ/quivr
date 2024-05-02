"use client";

import { useState } from "react";
import { useTranslation } from "react-i18next";

import { useUserApi } from "@/lib/api/user/useUserApi";
import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useUserData } from "@/lib/hooks/useUserData";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { ButtonType } from "@/lib/types/QuivrButton";

import { Settings } from "./components/Settings/Settings";
import styles from "./page.module.scss";

import { useLogoutModal } from "../../lib/hooks/useLogoutModal";

const UserPage = (): JSX.Element => {
  const { session } = useSupabase();
  const { userData } = useUserData();
  const { deleteUserData } = useUserApi();
  const { t } = useTranslation(["translation", "logout"]);
  const [deleteAccountModalOpened, setDeleteAccountModalOpened] =
    useState(false);
  const {
    handleLogout,
    isLoggingOut,
    isLogoutModalOpened,
    setIsLogoutModalOpened,
  } = useLogoutModal();

  const buttons: ButtonType[] = [
    {
      label: "Logout",
      color: "dangerous",
      onClick: () => {
        setIsLogoutModalOpened(true);
      },
      iconName: "logout",
    },
    {
      label: "Delete Account",
      color: "dangerous",
      onClick: () => {
        setDeleteAccountModalOpened(true);
      },
      iconName: "delete",
    },
  ];

  if (!session || !userData) {
    redirectToLogin();
  }

  return (
    <>
      <div className={styles.page_header}>
        <PageHeader iconName="user" label="Profile" buttons={buttons} />
      </div>
      <div className={styles.user_page_container}>
        <div className={styles.content_wrapper}>
          <Settings email={userData.email} />
        </div>
      </div>
      <Modal
        isOpen={isLogoutModalOpened}
        setOpen={setIsLogoutModalOpened}
        size="auto"
        CloseTrigger={<div />}
      >
        <div className={styles.modal_wrapper}>
          <h2>{t("areYouSure", { ns: "logout" })}</h2>
          <div className={styles.buttons}>
            <QuivrButton
              onClick={() => setIsLogoutModalOpened(false)}
              color="primary"
              label={t("cancel", { ns: "logout" })}
              iconName="close"
            ></QuivrButton>
            <QuivrButton
              isLoading={isLoggingOut}
              color="dangerous"
              onClick={() => void handleLogout()}
              label={t("logoutButton")}
              iconName="logout"
            ></QuivrButton>
          </div>
        </div>
      </Modal>
      <Modal
        isOpen={deleteAccountModalOpened}
        setOpen={setDeleteAccountModalOpened}
        size="auto"
        CloseTrigger={<div />}
      >
        <div className={styles.modal_wrapper}>
          <h2>Are you sure you want to delete your account ?</h2>
          <div className={styles.buttons}>
            <QuivrButton
              onClick={() => setDeleteAccountModalOpened(false)}
              color="primary"
              label={t("cancel", { ns: "logout" })}
              iconName="close"
            ></QuivrButton>
            <QuivrButton
              isLoading={isLoggingOut}
              color="dangerous"
              onClick={() => {
                void deleteUserData();
                void handleLogout();
              }}
              label="Delete Account"
              iconName="logout"
            ></QuivrButton>
          </div>
        </div>
      </Modal>
    </>
  );
};

export default UserPage;
