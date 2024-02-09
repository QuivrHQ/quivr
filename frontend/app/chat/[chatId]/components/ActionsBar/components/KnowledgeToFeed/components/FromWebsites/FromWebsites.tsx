import { useState } from "react";

import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

import styles from "./FromWebsites.module.scss";

export const FromWebsites = (): JSX.Element => {
  const [websiteValue, setWebsiteValue] = useState<string>("");

  return (
    <div className={styles.from_document_wrapper}>
      <TextInput
        label="Enter a website URL"
        setInputValue={setWebsiteValue}
        inputValue={websiteValue}
      />
    </div>
  );
};
