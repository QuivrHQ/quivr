import { FileIcon } from "react-file-icon";

import { SyncElement } from "@/lib/api/sync/types";
import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./CurrentFolderExplorerLine.module.scss";

// Fonction pour associer des extensions de fichier à des couleurs spécifiques
const getColorByExtension = (extension: string): string => {
  const extensionColorMap: { [key: string]: string } = {
    pdf: "#ffe5e5",
    doc: "#d0e0e3",
    docx: "#d0e0e3",
    txt: "#d8f0f5",
    xls: "#c0f4c0",
    xlsx: "#c0f4c0",
    csv: "#c0f4c0",
    ppt: "#fff7e5",
    pptx: "#fff7e5",
    jpg: "#f1f1fa",
    jpeg: "#f1f1fa",
    png: "#f1f1fa",
    gif: "#ffd4d8",
    mp3: "#ffe6d5",
    wav: "#ffe6d5",
    mp4: "#c0f4c0",
    mov: "#c0f4c0",
    zip: "#ededed",
    rar: "#ededed",
    js: "#fffde7",
    py: "#d8f0f5",
    html: "#ffebee",
    css: "#c0f4c0",
  };

  return extensionColorMap[extension] ?? "lightgrey";
};

interface CurrentFolderExplorerLineProps {
  element: SyncElement;
}

const CurrentFolderExplorerLine = ({
  element,
}: CurrentFolderExplorerLineProps): JSX.Element => {
  const extension = element.name?.split(".").pop()?.toLowerCase() ?? "file";
  const iconColor = getColorByExtension(extension);

  return (
    <div
      className={`${styles.folder_explorer_line_wrapper} ${
        element.is_folder ? styles.folder : ""
      }`}
    >
      <div className={styles.left}>
        {element.is_folder ? (
          <Icon name="folder" size="small" color="black" />
        ) : (
          <div className={styles.file_icon}>
            <FileIcon color={iconColor} extension={extension} />
          </div>
        )}
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
