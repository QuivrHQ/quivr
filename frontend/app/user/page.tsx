"use client";

import { useState } from "react";

import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { Tabs } from "@/lib/components/ui/Tabs/Tabs";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useUserData } from "@/lib/hooks/useUserData";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { Button } from "@/lib/types/QuivrButton";
import { Tab } from "@/lib/types/Tab";

import { BrainsUsage } from "./components/BrainsUsage/BrainsUsage";
import { LogoutModal } from "./components/LogoutModal/LogoutModal";
import { useLogoutModal } from "./components/LogoutModal/hooks/useLogoutModal";
import { Plan } from "./components/Plan/Plan";
import { Settings } from "./components/Settings/Settings";
import styles from "./page.module.scss";

const UserPage = (): JSX.Element => {
  const [selectedTab, setSelectedTab] = useState("Settings");
  const { session } = useSupabase();
  const { userData } = useUserData();
  const { isLogoutModalOpened, setIsLogoutModalOpened } = useLogoutModal();

  const button: Button = {
    label: "Logout",
    color: "dangerous",
    onClick: () => {
      setIsLogoutModalOpened(true);
    },
  };
  const userTabs: Tab[] = [
    {
      label: "Settings",
      isSelected: selectedTab === "Settings",
      onClick: () => setSelectedTab("Settings"),
    },
    {
      label: "Brains Usage",
      isSelected: selectedTab === "Brains Usage",
      onClick: () => setSelectedTab("Brains Usage"),
    },
    {
      label: "Plan",
      isSelected: selectedTab === "Plan",
      onClick: () => setSelectedTab("Plan"),
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
      <LogoutModal isLogoutModalOpened={isLogoutModalOpened} />
    </>
  );
};

export default UserPage;
