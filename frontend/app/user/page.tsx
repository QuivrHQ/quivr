"use client";

import { useTranslation } from "react-i18next";

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
  const { t } = useTranslation(["translation", "logout"]);
  const {
    handleLogout,
    isLoggingOut,
    isLogoutModalOpened,
    setIsLogoutModalOpened,
  } = useLogoutModal();

  const button: ButtonType = {
    label: "Logout",
    color: "dangerous",
    onClick: () => {
      setIsLogoutModalOpened(true);
    },
    iconName: "logout",
  };

  if (!session || !userData) {
    redirectToLogin();
  }

  return (
    <>
      <div className={styles.page_header}>
        <PageHeader iconName="user" label="Profile" buttons={[button]} />
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
        <div className="text-center flex flex-col items-center gap-5">
          <h2 className="text-lg font-medium mb-5">
            {t("areYouSure", { ns: "logout" })}
          </h2>
          <div className="flex gap-5 items-center justify-center">
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
    </>
  );
};

export default UserPage;
