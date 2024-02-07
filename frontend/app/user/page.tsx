"use client";

import { useState } from "react";
import { useTranslation } from "react-i18next";

import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { Modal } from "@/lib/components/ui/Modal";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useUserData } from "@/lib/hooks/useUserData";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { ButtonType } from "@/lib/types/QuivrButton";
import { Tab } from "@/lib/types/Tab";

import { BrainsUsage } from "./components/BrainsUsage/BrainsUsage";
import { Plan } from "./components/Plan/Plan";
import { Settings } from "./components/Settings/Settings";
import styles from "./page.module.scss";

import { useLogoutModal } from "../../lib/hooks/useLogoutModal";

const UserPage = (): JSX.Element => {
  const [selectedTab, setSelectedTab] = useState("Settings");
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
  const userTabs: Tab[] = [
    {
      label: "Settings",
      isSelected: selectedTab === "Settings",
      onClick: () => setSelectedTab("Settings"),
      iconName: "settings",
    },
    {
      label: "Brains Usage",
      isSelected: selectedTab === "Brains Usage",
      onClick: () => setSelectedTab("Brains Usage"),
      iconName: "graph",
    },
    {
      label: "Plan",
      isSelected: selectedTab === "Plan",
      onClick: () => setSelectedTab("Plan"),
      iconName: "star",
    },
  ];

  if (!session || !userData) {
    redirectToLogin();
  }

  return (
    <>
      <div className={styles.page_header}>
        <PageHeader iconName="user" label="Profile" buttons={[button]} />
      </div>
      <div className={styles.user_page_container}>
        <Tabs tabList={userTabs} />
        <div className={styles.content_wrapper}>
          {userTabs[0].isSelected && <Settings email={userData.email} />}
          {userTabs[1].isSelected && <BrainsUsage />}
          {userTabs[2].isSelected && <Plan />}
        </div>
      </div>
      <Modal
        isOpen={isLogoutModalOpened}
        setOpen={setIsLogoutModalOpened}
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
