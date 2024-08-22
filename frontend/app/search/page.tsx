"use client";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

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
      label: "Create brain",
      color: "primary",
      onClick: () => {
        setIsBrainCreationModalOpened(true);
      },
      iconName: "brain",
      tooltip:
        "You have reached the maximum number of brains allowed. Please upgrade your plan or delete some brains to create a new one.",
    },
  ]);

  const assistantsTabs: Tab[] = [
    {
      label: "Models",
      isSelected: selectedTab === "Models",
      onClick: () => setSelectedTab("Models"),
      iconName: "file",
    },
    {
      label: "Brains",
      isSelected: selectedTab === "Brains",
      onClick: () => setSelectedTab("Brains"),
      iconName: "settings",
    },
    {
      label: "All",
      isSelected: selectedTab === "All",
      onClick: () => setSelectedTab("All"),
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
          if (button.label === "Create brain") {
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

  return (
    <div className={styles.main_container}>
      <div className={styles.page_header}>
        <PageHeader iconName="home" label="Home" buttons={buttons} />
      </div>
      <div className={styles.search_page_container}>
        <div className={styles.main_wrapper}>
          <div className={styles.quivr_logo_wrapper}>
            <QuivrLogo size={80} color={isDarkMode ? "white" : "black"} />
            <div className={styles.quivr_text}>
              <span>Talk to </span>
              <span className={styles.quivr_text_primary}>{projectName ? projectName : "Quivr"}</span>
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
