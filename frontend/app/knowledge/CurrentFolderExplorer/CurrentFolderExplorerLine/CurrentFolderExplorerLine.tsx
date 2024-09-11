import { FileIcon } from "react-file-icon";

import { SyncElement } from "@/lib/api/sync/types";
import { Icon } from "@/lib/components/ui/Icon/Icon";

import styles from "./CurrentFolderExplorerLine.module.scss";

// Fonction pour associer des extensions de fichier à des couleurs spécifiques
const getColorByExtension = (extension: string): string => {
  const extensionColorMap: { [key: string]: string } = {
    // Documents
    pdf: "#db4437",
    doc: "#4285f4",
    docx: "#4285f4",
    txt: "#4285f4",

    // Feuilles de calcul
    xls: "#0f9d58",
    xlsx: "#0f9d58",
    csv: "#0f9d58",

    // Présentations
    ppt: "#f4b400",
    pptx: "#f4b400",

    // Images
    jpg: "#673ab7",
    jpeg: "#673ab7",
    png: "#673ab7",
    gif: "#ff63b6",

    // Audio
    mp3: "#f9ab00",
    wav: "#f9ab00",

    // Vidéo
    mp4: "#34a853",
    mov: "#34a853",

    // Archives
    zip: "#9e9e9e",
    rar: "#9e9e9e",

    // Code
    js: "#fbbc05",
    py: "#4285f4",
    html: "#ea4335",
    css: "#34a853",
  };

  return extensionColorMap[extension] ?? "gray";
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

export { CurrentFolderExplorerLine };
