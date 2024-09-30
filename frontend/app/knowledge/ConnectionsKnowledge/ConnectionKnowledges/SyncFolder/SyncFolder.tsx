import { useEffect, useState } from "react";

import { useKnowledgeContext } from "@/app/knowledge/KnowledgeProvider/hooks/useKnowledgeContext";
import { KMSElement } from "@/lib/api/sync/types";
import { useSync } from "@/lib/api/sync/useSync";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";

import styles from "./SyncFolder.module.scss";

interface SyncFolderProps {
  element: KMSElement;
}

const SyncFolder = ({ element }: SyncFolderProps): JSX.Element => {
  const [folded, setFolded] = useState(true);
  const [loading, setLoading] = useState(false);
  const { getSyncFiles } = useSync();
  const [syncElements, setKMSElements] = useState<KMSElement[]>();
  const [selectedFolder, setSelectedFolder] = useState<boolean>(false);

  const { currentFolder, setCurrentFolder, setQuivrRootSelected } =
    useKnowledgeContext();

  useEffect(() => {
    setSelectedFolder(currentFolder?.sync_file_id === element.sync_file_id);
    setQuivrRootSelected(false);
  }, [currentFolder]);

  useEffect(() => {
    if (!folded && element.sync_id !== null) {
      setLoading(true);
      void (async () => {
        try {
          if (element.sync_id === null || element.sync_file_id === null) {
            throw new Error("sync_id is null");
          }
          const res = await getSyncFiles(element.sync_id, element.sync_file_id);
          setKMSElements(res);
          setLoading(false);
        } catch (error) {
          console.error("Failed to get sync files:", error);
          setLoading(false);
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
            console.info(element);
            setCurrentFolder({
              ...element,
              parentKMSElement: element.parentKMSElement,
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
                      parentKMSElement: element,
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
