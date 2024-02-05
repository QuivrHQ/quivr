"use client";
import { usePathname } from "next/navigation";
import { useEffect } from "react";

import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { SearchBar } from "@/lib/components/ui/SearchBar/SearchBar";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";
import { Button } from "@/lib/types/QuivrButton";

import styles from "./page.module.scss";

const Search = (): JSX.Element => {
  const pathname = usePathname();
  const { session } = useSupabase();

  useEffect(() => {
    if (session === null) {
      redirectToLogin();
    }
  }, [pathname, session]);

  const buttons: Button[] = [
    {
      label: "Create brain",
      color: "primary",
      onClick: () => {
        console.info("create");
      },
    },
    {
      label: "Add knowledge",
      color: "primary",
      onClick: () => {
        console.info("add");
      },
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
    </div>
  );
};

export default Search;
