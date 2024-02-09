import { useCrawler } from "@/lib/components/KnowledgeToFeedInput/components/Crawler/hooks/useCrawler";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

import styles from "./FromWebsites.module.scss";

export const FromWebsites = (): JSX.Element => {
  const { handleSubmit, urlToCrawl, setUrlToCrawl } = useCrawler();

  return (
    <div className={styles.from_document_wrapper}>
      <TextInput
        label="Enter a website URL"
        setInputValue={setUrlToCrawl}
        inputValue={urlToCrawl}
        iconName="followUp"
        onSubmit={() => handleSubmit()}
      />
    </div>
  );
};
