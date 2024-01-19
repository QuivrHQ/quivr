"use client";

import { SearchBar } from "@/lib/components/ui/SearchBar/SearchBar";

import styles from "./page.module.scss"

const Search = (): JSX.Element => {
    return (
        <div className={styles.search_page_container}>

            <div className={styles.search_bar_container}>
                <SearchBar />
            </div>
        </div>
    );
};

export default Search;
