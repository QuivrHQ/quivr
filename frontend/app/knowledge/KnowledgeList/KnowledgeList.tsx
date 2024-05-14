"use client";

import { useState } from "react";

import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

import styles from "./KnowledgeList.module.scss";

const KnowledgeList = (): JSX.Element => {
  const [searchValue, setSearchValue] = useState<string>("");

  return (
    <div className={styles.knowledge_list_wrapper}>
      <div className={styles.search_bar}>
        <TextInput
          label="Search"
          iconName="search"
          inputValue={searchValue}
          setInputValue={setSearchValue}
        />
      </div>
    </div>
  );
};

export default KnowledgeList;
