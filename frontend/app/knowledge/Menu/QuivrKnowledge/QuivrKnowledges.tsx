import { useState } from "react";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";

import styles from "./QuivrKnowledges.module.scss";

import { useKnowledgeContext } from "../../KnowledgeProvider/hooks/useKnowledgeContext";

const QuivrKnowledges = (): JSX.Element => {
  const [folded, setFolded] = useState(true);
  const { isDarkMode } = useUserSettingsContext();
  const { setExploringQuivr, setCurrentFolder, setProviderRootSelected } =
    useKnowledgeContext();

  const { getFiles } = useKnowledgeApi();

  const fetchFiles = async () => {
    try {
      const res = await getFiles(null);
      console.info(res);
      setCurrentFolder(undefined);
      setProviderRootSelected(undefined);
      setExploringQuivr(true);
    } catch (error) {
      console.error("Failed to get files:", error);
    }
  };

  return (
    <div className={styles.header_section_wrapper}>
      <Icon
        name={folded ? "chevronRight" : "chevronDown"}
        size="normal"
        color="dark-grey"
        handleHover={true}
        onClick={() => setFolded(!folded)}
      />
      <div className={styles.hoverable} onClick={() => void fetchFiles()}>
        <QuivrLogo size={18} color={isDarkMode ? "white" : "black"} />
        <span className={styles.provider_title}>Quivr</span>
      </div>
    </div>
  );
};

export default QuivrKnowledges;
