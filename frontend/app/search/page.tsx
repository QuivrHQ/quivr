"use client";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { AddBrainModal } from "@/lib/components/AddBrainModal";
import { useBrainCreationContext } from "@/lib/components/AddBrainModal/brainCreation-provider";
import { OnboardingModal } from "@/lib/components/OnboardingModal/OnboardingModal";
import { PageHeader } from "@/lib/components/PageHeader/PageHeader";
import { UploadDocumentModal } from "@/lib/components/UploadDocumentModal/UploadDocumentModal";
import Icon from "@/lib/components/ui/Icon/Icon";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { SearchBar } from "@/lib/components/ui/SearchBar/SearchBar";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useOnboardingContext } from "@/lib/context/OnboardingProvider/hooks/useOnboardingContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { useUserData } from "@/lib/hooks/useUserData";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { ButtonType } from "@/lib/types/QuivrButton";

import BrainButton from "./BrainButton/BrainButton";
import styles from "./page.module.scss";

const Search = (): JSX.Element => {
  const [isUserDataFetched, setIsUserDataFetched] = useState(false);
  const [isNewBrain, setIsNewBrain] = useState(false);
  const [currentPage, setCurrentPage] = useState(0);
  const [transitionDirection, setTransitionDirection] = useState("");
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

  const newBrain = () => {
    setIsNewBrain(true);
    setTimeout(() => {
      setIsNewBrain(false);
    }, 750);
  };

  const totalPages = Math.ceil(allBrains.length / brainsPerPage);

  const handleNextPage = () => {
    if (currentPage < totalPages - 1) {
      setTransitionDirection("next");
      setCurrentPage((prevPage) => prevPage + 1);
    }
  };

  const handlePreviousPage = () => {
    if (currentPage > 0) {
      setTransitionDirection("prev");
      setCurrentPage((prevPage) => prevPage - 1);
    }
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
              disabled: userData.max_brains <= allBrains.length,
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

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (document.activeElement) {
        const tagName = document.activeElement.tagName.toLowerCase();
        if (tagName !== "body") {
          return;
        }
      }

      switch (event.key) {
        case "ArrowLeft":
          handlePreviousPage();
          break;
        case "ArrowRight":
          handleNextPage();
          break;
        default:
          break;
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [handlePreviousPage, handleNextPage]);

  const displayedBrains = allBrains.slice(
    currentPage * brainsPerPage,
    (currentPage + 1) * brainsPerPage
  );

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
            <div className={styles.brains_list_container}>
              <div
                className={`${styles.chevron} ${
                  currentPage === 0 ? styles.disabled : ""
                }`}
                onClick={handlePreviousPage}
              >
                <Icon
                  name="chevronLeft"
                  size="big"
                  color="black"
                  handleHover={true}
                />
              </div>
              <div
                className={`${styles.brains_list_wrapper} ${
                  transitionDirection === "next"
                    ? styles.slide_next
                    : styles.slide_prev
                }`}
              >
                {displayedBrains.map((brain, index) => (
                  <BrainButton key={index} brain={brain} newBrain={newBrain} />
                ))}
              </div>
              <div
                className={`${styles.chevron} ${
                  currentPage >= totalPages - 1 ? styles.disabled : ""
                }`}
                onClick={handleNextPage}
              >
                <Icon
                  name="chevronRight"
                  size="big"
                  color="black"
                  handleHover={true}
                />
              </div>
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
