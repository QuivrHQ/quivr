import { useEffect, useState } from "react";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";

import styles from "./QuivrKnowledges.module.scss";

const QuivrKnowledges = (): JSX.Element => {
  const [folded, setFolded] = useState(true);
  const { isDarkMode } = useUserSettingsContext();

  const { getFiles } = useKnowledgeApi();

  useEffect(() => {
    void (async () => {
      try {
        const res = await getFiles(null);
        console.info(res);
      } catch (error) {
        console.error("Failed to get files:", error);
      }
    })();
  }, [folded]);

  return (
    <div
      className={styles.header_section_wrapper}
      onClick={() => setFolded(!folded)}
    >
      <Icon
        name={folded ? "chevronRight" : "chevronDown"}
        size="normal"
        color="dark-grey"
        handleHover={true}
      />
      <QuivrLogo size={18} color={isDarkMode ? "white" : "black"} />
      <span className={styles.provider_title}>Quivr</span>
    </div>
  );
};

export default QuivrKnowledges;
