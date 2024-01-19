"use client";

import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { SearchBar } from "@/lib/components/ui/SearchBar/SearchBar";
import { ChatProvider } from "@/lib/context";

import styles from "./page.module.scss"

const Search = (): JSX.Element => {
    return (
        <ChatProvider>
            <div className={styles.search_page_container}>
                <div className={styles.main_container}>
                    <div className={styles.quivr_logo_wrapper}>
                        <QuivrLogo size={80} color="black" />
                        <div className={styles.quivr_text}>
                            <span>Talk to </span>
                            <span className={styles.quivr_text_primary}>Quivr</span>
                        </div>
                    </div>
                    <SearchBar />
                </div>
            </div >
        </ChatProvider>
    );
};

export default Search;
