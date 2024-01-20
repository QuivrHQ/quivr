"use client";
import { usePathname } from "next/navigation";
import { useEffect } from "react";

import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { SearchBar } from "@/lib/components/ui/SearchBar/SearchBar";
import { useMenuContext } from "@/lib/context/MenuProvider/hooks/useMenuContext";

import styles from "./page.module.scss";

const Search = (): JSX.Element => {
    const {setIsOpened} = useMenuContext();
    const pathname = usePathname()

    useEffect(() => {
        setIsOpened(false);
    }, [pathname]);

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
                <SearchBar />
            </div>
        </div >
    );
};

export default Search;
