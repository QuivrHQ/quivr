"use client";
import { usePathname } from "next/navigation";
import { useEffect } from "react";

import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { AddBrainModal } from "@/lib/components/AddBrainModal";
import { useBrainCreationContext } from "@/lib/components/AddBrainModal/components/AddBrainSteps/brainCreation-provider";
import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { UploadDocumentModal } from "@/lib/components/UploadDocumentModal/UploadDocumentModal";
import { SearchBar } from "@/lib/components/ui/SearchBar/SearchBar";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { ButtonType } from "@/lib/types/QuivrButton";

import styles from "./page.module.scss";

const Search = (): JSX.Element => {
  const pathname = usePathname();
  const { session } = useSupabase();
  const { setIsBrainCreationModalOpened } = useBrainCreationContext();

  useEffect(() => {
    if (session === null) {
      redirectToLogin();
    }
  }, [pathname, session]);

  const buttons: ButtonType[] = [
    {
      label: "Create brain",
      color: "primary",
      onClick: () => {
        setIsBrainCreationModalOpened(true);
      },
      iconName: "brain",
    },
  ];

  return (
    <div className={styles.main_container}>
      <div className={styles.page_header}>
        <PageHeader iconName="home" label="Home" buttons={buttons} />
      </div>
      <div className={styles.search_page_container}>
        <div className={styles.main_wrapper}>
          <div className={styles.quivr_logo_wrapper}>
            <QuivrLogo size={80} color="black" />
            <div className={styles.quivr_text}>
              <span>Talk to </span>
              <span className={styles.quivr_text_primary}>Quivr</span>
            </div>
          </div>
          <div className={styles.search_bar_wrapper}>
            <SearchBar />
          </div>
        </div>
        <div className={styles.shortcuts_card_wrapper}>
          <div className={styles.shortcut_wrapper}>
            <span className={styles.shortcut}>@</span>
            <span>Select a brain</span>
          </div>
          <div className={styles.shortcut_wrapper}>
            <span className={styles.shortcut}>#</span>
            <span>Select a prompt</span>
          </div>
        </div>
      </div>
      <UploadDocumentModal />
      <AddBrainModal />
    </div>
  );
};

export default Search;
