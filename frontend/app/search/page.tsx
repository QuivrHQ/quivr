"use client";

import { SearchBar } from "@/lib/components/ui/SearchBar/SearchBar";
import "./page.scss"

const Search = (): JSX.Element => {
    return (
        <div className="search_page_container">
            <div className="search_bar_wrapper">
                <SearchBar />
            </div>
        </div>
    );
};

export default Search;
