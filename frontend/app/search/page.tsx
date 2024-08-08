"use client";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { AddBrainModal } from "@/lib/components/AddBrainModal";
import { useBrainCreationContext } from "@/lib/components/AddBrainModal/brainCreation-provider";
import { OnboardingModal } from "@/lib/components/OnboardingModal/OnboardingModal";
import { PageHeader } from "@/lib/components/PageHeader/PageHeader";
import { UploadDocumentModal } from "@/lib/components/UploadDocumentModal/UploadDocumentModal";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { SearchBar } from "@/lib/components/ui/SearchBar/SearchBar";
import { SmallTabs } from "@/lib/components/ui/SmallTabs/SmallTabs";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useOnboardingContext } from "@/lib/context/OnboardingProvider/hooks/useOnboardingContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { useUserData } from "@/lib/hooks/useUserData";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { ButtonType } from "@/lib/types/QuivrButton";
import { Tab } from "@/lib/types/Tab";

import BrainsList from "./BrainsList/BrainsList";
import styles from "./page.module.scss";

const Search = (): JSX.Element => {
  const [selectedTab, setSelectedTab] = useState("Models");
  const [isUserDataFetched, setIsUserDataFetched] = useState(false);
  const [isNewBrain, setIsNewBrain] = useState(false);
  const brainsPerPage = 6;

  const pathname = usePathname();
  const { session } = useSupabase();
  const { isBrainCreationModalOpened, setIsBrainCreationModalOpened } =
    useBrainCreationContext();
  const { userIdentityData, userData } = useUserData();
  const { isDarkMode } = useUserSettingsContext();
  const { isBrainCreated } = useOnboardingContext();
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
    if (userIdentityData) {
      setIsUserDataFetched(true);
    }
  }, [userIdentityData]);

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
    <>
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
                <span className={styles.quivr_text_primary}>Quivr</span>
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
      {!isBrainCreationModalOpened &&
        !userIdentityData?.onboarded &&
        !isBrainCreated &&
        !!isUserDataFetched && (
          <div className={styles.onboarding_overlay}>
            <div className={styles.main_message_wrapper}>
              <MessageInfoBox type="tutorial">
                <div className={styles.main_message}>
                  <span>Welcome {userIdentityData?.username}!</span>
                  <span>
                    We will guide you through your quivr adventure and the
                    creation of your first brain.
                  </span>
                  <span className={styles.bolder}>
                    First, Press the Create Brain button on the top right corner
                    to create your first brain.
                  </span>
                </div>
              </MessageInfoBox>
            </div>
            <div className={styles.first_brain_button}>
              <QuivrButton
                iconName="brain"
                label="Create Brain"
                color="primary"
                onClick={() => {
                  setIsBrainCreationModalOpened(true);
                }}
              />
            </div>
          </div>
        )}
    </>
  );
};

export default Search;
