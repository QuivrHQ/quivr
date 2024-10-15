import { useState } from "react";

import { KMSElement } from "@/lib/api/sync/types";
import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { iconList } from "@/lib/helpers/iconList";

import ConnectedBrains from "./ConnectedBrains/ConnectedBrains";
import styles from "./CurrentFolderExplorerLine.module.scss";

import { useKnowledgeContext } from "../../../KnowledgeProvider/hooks/useKnowledgeContext";

interface CurrentFolderExplorerLineProps {
  element: KMSElement;
  onDragStart?: (
    event: React.DragEvent<HTMLDivElement>,
    element: KMSElement
  ) => void;
  onDrop?: (
    event: React.DragEvent<HTMLDivElement>,
    element: KMSElement
  ) => void;
  onDragOver?: (event: React.DragEvent<HTMLDivElement>) => void;
}

const getFileType = (fileName?: string): string => {
  return fileName?.includes(".")
    ? fileName.split(".").pop()?.toLowerCase() ?? "default"
    : "default";
};

const getIconColor = (fileType: string): string => {
  const iconColors: { [key: string]: string } = {
    pdf: "#E44A4D",

    csv: "#4EB35E",
    xlsx: "#4EB35E",
    xls: "#4EB35E",

    docx: "#47A8EF",
    doc: "#47A8EF",
    docm: "#47A8EF",

    png: "#A36BAD",
    jpg: "#A36BAD",

    pptx: "#F07114",
    ppt: "#F07114",

    mp3: "#FFC220",
    mp4: "#FFC220",
    wav: "#FFC220",

    html: "#F16529",
    py: "#F16529",
  };

  return iconColors[fileType.toLowerCase()] ?? "#B1B9BE";
};

const getIconName = (element: KMSElement, fileType: string): string => {
  return element.url
    ? "link"
    : element.is_folder
    ? "folder"
    : fileType !== "default"
    ? iconList[fileType.toLocaleLowerCase()]
      ? fileType.toLowerCase()
      : "file"
    : "file";
};

const CurrentFolderExplorerLine = ({
  element,
  onDragStart,
  onDrop,
  onDragOver,
}: CurrentFolderExplorerLineProps): JSX.Element => {
  const { setCurrentFolder } = useKnowledgeContext();
  const { selectedKnowledges, setSelectedKnowledges } = useKnowledgeContext();
  const [isDraggedOver, setIsDraggedOver] = useState(false);

  const fileType = getFileType(element.file_name);

  const handleCheckboxChange = (checked: boolean) => {
    if (checked) {
      setSelectedKnowledges([...selectedKnowledges, element]);
    } else {
      setSelectedKnowledges(
        selectedKnowledges.filter((knowledge) => knowledge.id !== element.id)
      );
    }
  };

  const handleClick = () => {
    if (element.is_folder) {
      setCurrentFolder({
        ...element,
        parentKMSElement: element.parentKMSElement,
      });
    }
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    onDrop?.(event, element);
    setIsDraggedOver(false);
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    onDragOver?.(event);
    setIsDraggedOver(true);
  };

  return (
    <div
      className={`${styles.folder_explorer_line_wrapper} ${
        element.is_folder ? styles.folder : ""
      } ${isDraggedOver && element.is_folder ? styles.dragged : ""}`}
      onClick={handleClick}
      draggable
      onDragStart={(event) => onDragStart?.(event, element)}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={() => setIsDraggedOver(false)}
    >
      <div className={styles.left}>
        <div className={styles.checkbox}>
          {element.source === "local" && (
            <Checkbox
              checked={selectedKnowledges.includes(element)}
              setChecked={(checked) => handleCheckboxChange(checked)}
            />
          )}
        </div>
        <Icon
          name={getIconName(element, fileType)}
          size="small"
          customColor={getIconColor(fileType)}
          color={element.is_folder ? "black" : undefined}
        />
        <span
          className={`${styles.name} ${element.url ? styles.url : ""}`}
          onClick={(event) => {
            if (element.url) {
              event.stopPropagation();
              window.open(element.url, "_blank");
            }
          }}
        >
          {element.file_name ?? element.url}
        </span>
      </div>
      <div className={styles.right}>
        <ConnectedBrains connectedBrains={element.brains} knowledge={element} />
        <div className={element.is_folder ? styles.visible : styles.hidden}>
          <Icon
            name="chevronRight"
            size="normal"
            color="black"
            handleHover={true}
          />
        </div>
      </div>
    </div>
  );
};

export default CurrentFolderExplorerLine;
