import { SyncElement } from "@/lib/api/sync/types";
import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./CurrentFolderExplorerLine.module.scss";

import { useKnowledgeContext } from "../../KnowledgeProvider/hooks/useKnowledgeContext";

interface CurrentFolderExplorerLineProps {
  element: SyncElement;
}

const CurrentFolderExplorerLine = ({
  element,
}: CurrentFolderExplorerLineProps): JSX.Element => {
  const { setCurrentFolder } = useKnowledgeContext();

  const extension = element.name?.split(".").pop()?.toLowerCase() ?? "file";

  return (
    <div
      className={`${styles.folder_explorer_line_wrapper} ${
        element.is_folder ? styles.folder : ""
      }`}
      onClick={() => {
        if (element.is_folder) {
          setCurrentFolder(element);
        }
      }}
    >
      <div className={styles.left}>
        <Icon
          name={element.is_folder ? "folder" : "file"}
          size="small"
          color="black"
        />
        <span className={styles.name}>{element.name}</span>
      </div>
      {element.is_folder && (
        <Icon
          name="chevronRight"
          size="normal"
          color="black"
          handleHover={true}
        />
      )}
    </div>
  );
};

export default CurrentFolderExplorerLine;
