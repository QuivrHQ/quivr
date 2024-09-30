import { useEffect, useState } from "react";

import { useKnowledgeContext } from "@/app/knowledge/KnowledgeProvider/hooks/useKnowledgeContext";
import { SyncElement } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";

import styles from "./SyncFolder.module.scss";

interface SyncFolderProps {
  element: SyncElement;
}

const SyncFolder = ({ element }: SyncFolderProps): JSX.Element => {
  const [folded, setFolded] = useState(true);
  const [loading, setLoading] = useState(false);
  const { getSyncFiles } = useSync();
  const [syncElements, setSyncElements] = useState<SyncElement[]>();
  const [selectedFolder, setSelectedFolder] = useState<boolean>(false);

  const { currentFolder, setCurrentFolder } = useKnowledgeContext();

  useEffect(() => {
    setSelectedFolder(currentFolder?.sync_file_id === element.sync_file_id);
  }, [currentFolder]);

  useEffect(() => {
    if (!folded) {
      setLoading(true);
      void (async () => {
        try {
          const res = await getSyncFiles(element.sync_id, element.sync_file_id);
          setSyncElements(res);
          setLoading(false);
        } catch (error) {
          console.error("Failed to get sync files:", error);
        }
      })();
    }
  }, [folded]);

  return (
    <div
      className={`${styles.folder_wrapper} ${
        !syncElements?.filter((file) => file.is_folder).length && !loading
          ? styles.empty
          : ""
      }`}
    >
      <div className={styles.folder_line_wrapper}>
        <Icon
          name={folded ? "chevronRight" : "chevronDown"}
          size="normal"
          color="dark-grey"
          handleHover={true}
          onClick={() => setFolded(!folded)}
        />
        <span
          className={`${styles.name} ${selectedFolder ? styles.selected : ""}`}
          onClick={() => {
            setCurrentFolder({
              ...element,
              parentSyncElement: element.parentSyncElement,
            });
          }}
        >
          {element.file_name?.includes(".")
            ? element.file_name.split(".").slice(0, -1).join(".")
            : element.file_name}
        </span>
      </div>
      {!folded &&
        (loading ? (
          <div className={styles.loader_icon}>
            <LoaderIcon color="primary" size="small" />
          </div>
        ) : (
          <div className={styles.sync_elements_wrapper}>
            {syncElements
              ?.filter((file) => file.is_folder)
              .map((folder, id) => (
                <div key={id}>
                  <SyncFolder
                    element={{
                      ...folder,
                      parentSyncElement: element,
                    }}
                  />
                </div>
              ))}
          </div>
        ))}
    </div>
  );
};

export default SyncFolder;
