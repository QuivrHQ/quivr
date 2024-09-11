import { useEffect, useState } from "react";

import { useKnowledgeContext } from "@/app/knowledge/KnowledgeProvider/hooks/useKnowledgeContext";
import { SyncElement, SyncElements } from "@/lib/api/sync/types";
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
  const [syncElements, setSyncElements] = useState<SyncElements>();
  const [selectedFolder, setSelectedFolder] = useState<boolean>(false);

  const { currentFolder, setCurrentFolder } = useKnowledgeContext();

  useEffect(() => {
    setSelectedFolder(currentFolder?.id === element.id);
  }, [currentFolder]);

  useEffect(() => {
    if (!folded) {
      setLoading(true);
      void (async () => {
        try {
          const res = await getSyncFiles(element.syncId, element.id);
          setSyncElements((prevState) => ({
            ...prevState,
            files: res.files.map((syncElement) => ({
              ...syncElement,
              syncId: element.syncId,
            })),
          }));
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
        !syncElements?.files.filter((file) => file.is_folder).length && !loading
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
          onClick={() => setCurrentFolder(element)}
        >
          {element.name?.includes(".")
            ? element.name.split(".").slice(0, -1).join(".")
            : element.name}
        </span>
      </div>
      {!folded &&
        (loading ? (
          <div className={styles.loader_icon}>
            <LoaderIcon color="primary" size="small" />
          </div>
        ) : (
          <div className={styles.sync_elements_wrapper}>
            {syncElements?.files
              .filter((file) => file.is_folder)
              .map((folder, id) => (
                <div key={id}>
                  <SyncFolder element={folder} />
                </div>
              ))}
          </div>
        ))}
    </div>
  );
};

export default SyncFolder;
