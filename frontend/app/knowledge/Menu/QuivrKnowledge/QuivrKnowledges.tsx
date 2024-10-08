import { useEffect, useState } from "react";

import { useKnowledgeApi } from "@/lib/api/knowledge/useKnowledgeApi";
import { KMSElement } from "@/lib/api/sync/types";
import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { handleDrop } from "@/lib/helpers/kms";

import QuivrFolder from "./QuivrFolder/QuivrFolder";
import styles from "./QuivrKnowledges.module.scss";

import { useKnowledgeContext } from "../../KnowledgeProvider/hooks/useKnowledgeContext";

const QuivrKnowledges = (): JSX.Element => {
  const [folded, setFolded] = useState(true);
  const [kmsElements, setKMSElements] = useState<KMSElement[]>();
  const [loading, setLoading] = useState(false);
  const { isDarkMode } = useUserSettingsContext();
  const {
    setExploringQuivr,
    setCurrentFolder,
    setExploredProvider,
    setRefetchFolderMenu,
    refetchFolderMenu,
    currentFolder,
  } = useKnowledgeContext();

  const { getFiles, patchKnowledge } = useKnowledgeApi();

  const chooseQuivrRoot = () => {
    setCurrentFolder(undefined);
    setExploredProvider(undefined);
    setExploringQuivr(true);
  };

  const fetchFiles = async () => {
    setLoading(true);
    try {
      const res = await getFiles(null);
      setKMSElements(res);
    } catch (error) {
      console.error("Failed to get sync files:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void fetchFiles();
  }, []);

  useEffect(() => {
    if (refetchFolderMenu) {
      void fetchFiles();
      setRefetchFolderMenu(false);
    }
  }, [refetchFolderMenu]);

  return (
    <div className={styles.main_container}>
      <div
        className={styles.header_section_wrapper}
        onDrop={(event) =>
          void handleDrop({
            event,
            targetElement: null,
            patchKnowledge,
            setRefetchFolderMenu,
            currentFolder,
          })
        }
      >
        <Icon
          name={folded ? "chevronRight" : "chevronDown"}
          size="normal"
          color="dark-grey"
          handleHover={true}
          onClick={() => setFolded(!folded)}
        />
        <div
          className={styles.hoverable}
          onClick={() => void chooseQuivrRoot()}
        >
          <QuivrLogo size={18} color={isDarkMode ? "white" : "black"} />
          <span className={styles.provider_title}>Quivr</span>
        </div>
      </div>
      {!folded ? (
        loading ? (
          <div className={styles.loader_icon}>
            <LoaderIcon color="primary" size="small" />
          </div>
        ) : (
          <div
            className={`${styles.sync_elements_wrapper} ${
              !kmsElements?.filter((file) => file.is_folder).length
                ? styles.empty
                : ""
            } `}
          >
            {kmsElements
              ?.filter((file) => file.is_folder)
              .map((element, id) => (
                <div key={id}>
                  <QuivrFolder element={element} />
                </div>
              ))}
          </div>
        )
      ) : null}
    </div>
  );
};

export default QuivrKnowledges;
