/* eslint-disable max-lines */
"use client";

import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { useUserApi } from "@/lib/api/user/useUserApi";
import { PageHeader } from "@/lib/components/PageHeader/PageHeader";
import { Modal } from "@/lib/components/ui/Modal/Modal";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { useUserData } from "@/lib/hooks/useUserData";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { ButtonType } from "@/lib/types/QuivrButton";
import { Tab } from "@/lib/types/Tab";

import { Connections } from "./components/Connections/Connections";
import { ResetPassword } from "./components/ResetPassword/ResetPassword";
import { Settings } from "./components/Settings/Settings";
import styles from "./page.module.scss";

import { useLogoutModal } from "../../lib/hooks/useLogoutModal";

const UserPage = (): JSX.Element => {
  const { session } = useSupabase();
  const { userData, userIdentityData } = useUserData();
  const { deleteUserData, getUserCredits } = useUserApi();
  const { t } = useTranslation(["translation", "logout", "user"]);
  const [deleteAccountModalOpened, setDeleteAccountModalOpened] =
    useState(false);
  const [resetPasswordModalOpened, setResetPasswordModalOpened] =
    useState(false);
  const {
    handleLogout,
    isLoggingOut,
    isLogoutModalOpened,
    setIsLogoutModalOpened,
  } = useLogoutModal();
  const [selectedTab, setSelectedTab] = useState("General");
  const { remainingCredits, setRemainingCredits } = useUserSettingsContext();

  useEffect(() => {
    void (async () => {
      const res = await getUserCredits();
      setRemainingCredits(res);
    })();
  }, []);

  const buttons: ButtonType[] = [
    {
      label: t("reset_password", { ns: "user" }),
      color: "primary",
      onClick: () => {
        setResetPasswordModalOpened(true);
      },
      iconName: "settings",
    },
    {
      label: t("title", { ns: "logout" }),
      color: "dangerous",
      onClick: () => {
        setIsLogoutModalOpened(true);
      },
      iconName: "logout",
    },
    {
      label: t("delete_account", { ns: "translation" }),
      color: "dangerous",
      onClick: () => {
        setDeleteAccountModalOpened(true);
      },
      iconName: "delete",
    },
  ];

  const studioTabs: Tab[] = [
    {
      label: t("general", { ns: "translation" }),
      isSelected: selectedTab === "General",
      onClick: () => setSelectedTab("General"),
      iconName: "user",
    },
    {
      label: t("connections", { ns: "translation" }),
      isSelected: selectedTab === "Connections",
      onClick: () => setSelectedTab("Connections"),
      iconName: "sync",
    },
  ];

  if (!session || !userData) {
    redirectToLogin();
  }

  return (
    <>
      <div className={styles.page_header}>
        <PageHeader iconName='user' label='Hồ sơ' buttons={buttons} />
      </div>
      <div className={styles.user_page_container}>
        <Tabs tabList={studioTabs} />
        <div className={styles.user_page_menu}></div>
        <div className={styles.content_wrapper}>
          {selectedTab === "General" && (
            <Settings
              email={userData.email}
              username={userIdentityData?.username ?? ""}
              remainingCredits={remainingCredits ?? 0}
            />
          )}
          {selectedTab === "Connections" && <Connections />}
        </div>
      </div>

      {/* Reset password modal */}
      <Modal
        isOpen={resetPasswordModalOpened}
        setOpen={setResetPasswordModalOpened}
        size='auto'
        CloseTrigger={<div />}
      >
        <ResetPassword onClose={() => setResetPasswordModalOpened(false)} />
      </Modal>

      <Modal
        isOpen={isLogoutModalOpened}
        setOpen={setIsLogoutModalOpened}
        size='auto'
        CloseTrigger={<div />}
      >
        <div className={styles.modal_wrapper}>
          <h2>{t("areYouSure", { ns: "logout" })}</h2>
          <div className={styles.buttons}>
            <QuivrButton
              onClick={() => setIsLogoutModalOpened(false)}
              color='primary'
              label={t("cancel", { ns: "logout" })}
              iconName='close'
            ></QuivrButton>
            <QuivrButton
              isLoading={isLoggingOut}
              color='dangerous'
              onClick={() => void handleLogout()}
              label={t("logoutButton")}
              iconName='logout'
            ></QuivrButton>
          </div>
        </div>
      </Modal>
      <Modal
        isOpen={deleteAccountModalOpened}
        setOpen={setDeleteAccountModalOpened}
        size='auto'
        CloseTrigger={<div />}
      >
        <div className={styles.modal_wrapper}>
          <h2>{t("delete_account_description", { ns: "user" })}</h2>
          <div className={styles.buttons}>
            <QuivrButton
              onClick={() => setDeleteAccountModalOpened(false)}
              color='primary'
              label={t("cancel", { ns: "logout" })}
              iconName='close'
            ></QuivrButton>
            <QuivrButton
              isLoading={isLoggingOut}
              color='dangerous'
              onClick={() => {
                void deleteUserData();
                void handleLogout();
              }}
              label={t("delete_account", { ns: "user" })}
              iconName='logout'
            ></QuivrButton>
          </div>
        </div>
      </Modal>
    </>
  );
};

export default UserPage;
