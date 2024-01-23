"use client";
import { usePathname } from "next/navigation";
import { useEffect } from "react";

import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { AddBrainModal } from "@/lib/components/AddBrainModal";
import { SearchBar } from "@/lib/components/ui/SearchBar/SearchBar";
import { useMenuContext } from "@/lib/context/MenuProvider/hooks/useMenuContext";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import styles from "./page.module.scss";

import { useChatsList } from "../chat/[chatId]/hooks/useChatsList";


const Search = (): JSX.Element => {
  const { setIsOpened } = useMenuContext();
  const pathname = usePathname();
  const { session } = useSupabase();

  useEffect(() => {
    if (session === null) {
      redirectToLogin();
    }
    setIsOpened(false);
  }, [pathname, session, setIsOpened]);

  useChatsList();

  return (
    <div className={styles.search_page_container}>
      <div className={styles.main_container}>
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
      <div className={styles.add_brain_wrapper}>
        <AddBrainModal />
      </div>
    </div>
  );
};

export default Search;
