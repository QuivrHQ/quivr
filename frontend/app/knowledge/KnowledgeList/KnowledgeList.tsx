"use client";

import { useState } from "react";

import { TextInput } from "@/lib/components/ui/TextInput/TextInput";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import BrainFolder from "./BrainFolder/BrainFolder";
import styles from "./KnowledgeList.module.scss";

const KnowledgeList = (): JSX.Element => {
  const [searchValue, setSearchValue] = useState<string>("");
  const { allBrains } = useBrainContext();

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
      {allBrains.map((brain) => (
        <div key={brain.id}>
          <BrainFolder brain={brain} />
        </div>
      ))}
    </div>
  );
};

export default KnowledgeList;
