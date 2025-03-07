"use client";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { AddBrainModal } from "@/lib/components/AddBrainModal";
import { useBrainCreationContext } from "@/lib/components/AddBrainModal/brainCreation-provider";
import { OnboardingModal } from "@/lib/components/OnboardingModal/OnboardingModal";
import { PageHeader } from "@/lib/components/PageHeader/PageHeader";
import { UploadDocumentModal } from "@/lib/components/UploadDocumentModal/UploadDocumentModal";
import { SearchBar } from "@/lib/components/ui/SearchBar/SearchBar";
import { SmallTabs } from "@/lib/components/ui/SmallTabs/SmallTabs";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { useUserData } from "@/lib/hooks/useUserData";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { ButtonType } from "@/lib/types/QuivrButton";
import { Tab } from "@/lib/types/Tab";

import BrainsList from "./BrainsList/BrainsList";
import styles from "./page.module.scss";

const projectName = process.env.NEXT_PUBLIC_PROJECT_NAME;

const Search = (): JSX.Element => {
  const { t } = useTranslation(["login", "chat", "brain", "translation"]);

  const [selectedTab, setSelectedTab] = useState("Models");
  const [isNewBrain, setIsNewBrain] = useState(false);
  const brainsPerPage = 6;

  const pathname = usePathname();
  const { session } = useSupabase();
  const { setIsBrainCreationModalOpened } = useBrainCreationContext();
  const { userData } = useUserData();
  const { isDarkMode } = useUserSettingsContext();
  const { allBrains } = useBrainContext();

  const [buttons, setButtons] = useState<ButtonType[]>([
    {
      label: t("createBrain", { ns: "brain" }),
      color: "primary",
      onClick: () => {
        setIsBrainCreationModalOpened(true);
      },
      iconName: "brain",
      tooltip: t("tooltip_brain_maximum_number", { ns: "brain" }),
    },
  ]);

  const assistantsTabs: Tab[] = [
    {
      label: t("models", { ns: "translation" }),
      isSelected: selectedTab === t("models", { ns: "translation" }),
      onClick: () => setSelectedTab(t("models", { ns: "translation" })),
      iconName: "file",
    },
    {
      label: t("brains", { ns: "translation" }),
      isSelected: selectedTab === t("brains", { ns: "translation" }),
      onClick: () => setSelectedTab(t("brains", { ns: "translation" })),
      iconName: "settings",
    },
    {
      label: t("all", { ns: "translation" }),
      isSelected: selectedTab === t("all", { ns: "translation" }),
      onClick: () => setSelectedTab(t("all", { ns: "translation" })),
      iconName: "settings",
    },
  ];

  const newBrain = () => {
    setIsNewBrain(true);
    setTimeout(() => {
      setIsNewBrain(false);
    }, 750);
  };

  useEffect(() => {
    if (userData) {
      setButtons((prevButtons) => {
        return prevButtons.map((button) => {
          if (button.label === t("createBrain", { ns: "brain" })) {
            return {
              ...button,
              disabled:
                userData.max_brains <=
                allBrains.filter((brain) => brain.brain_type === "doc").length,
            };
          }

          return button;
        });
      });
    }
  }, [userData?.max_brains, allBrains.length]);

  useEffect(() => {
    if (session === null) {
      redirectToLogin();
    }
  }, [pathname, session]);

  console.log("session", session);
  console.log("userData", userData);

  return (
    <div className={styles.main_container}>
      <div className={styles.page_header}>
        <PageHeader
          iconName='home'
          label={t("home", { ns: "chat" })}
          buttons={buttons}
        />
      </div>
      <div className={styles.search_page_container}>
        <div className={styles.main_wrapper}>
          <div className={styles.quivr_logo_wrapper}>
            <QuivrLogo size={80} color={isDarkMode ? "white" : "black"} />
            <div className={styles.quivr_text}>
              <span>{t("talk_to", { ns: "login" })} </span>
              <span className={styles.quivr_text_primary}>
                {projectName ? projectName : "Dobbie"}
              </span>
            </div>
          </div>
          <div className={styles.search_bar_wrapper}>
            <SearchBar newBrain={isNewBrain} />
          </div>
          <div className={styles.assistants_container}>
            <div className={styles.tabs}>
              <SmallTabs tabList={assistantsTabs} />
            </div>
            <BrainsList
              brains={allBrains}
              selectedTab={selectedTab}
              brainsPerPage={brainsPerPage}
              newBrain={newBrain}
            />
          </div>
        </div>
      </div>
      <UploadDocumentModal />
      <AddBrainModal />
      <OnboardingModal />
    </div>
  );
};

export default Search;
