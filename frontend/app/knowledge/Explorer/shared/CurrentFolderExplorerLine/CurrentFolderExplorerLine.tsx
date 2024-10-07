import { KMSElement } from "@/lib/api/sync/types";
import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { iconList } from "@/lib/helpers/iconList";

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

const CurrentFolderExplorerLine = ({
  element,
  onDragStart,
  onDrop,
  onDragOver,
}: CurrentFolderExplorerLineProps): JSX.Element => {
  const { setCurrentFolder } = useKnowledgeContext();
  const { selectedKnowledges, setSelectedKnowledges } = useKnowledgeContext();

  const fileType = element.file_name?.includes(".")
    ? element.file_name.split(".").pop()?.toLowerCase() ?? "default"
    : "default";

  const getIconColor = (): string => {
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

    const fileTypeLowerCase = fileType.toLowerCase();

    return iconColors[fileTypeLowerCase] ?? "#B1B9BE";
  };

  const handleCheckboxChange = (checked: boolean) => {
    if (checked) {
      setSelectedKnowledges([...selectedKnowledges, element]);
    } else {
      setSelectedKnowledges(
        selectedKnowledges.filter((knowledge) => knowledge.id !== element.id)
      );
    }
  };

  return (
    <div
      className={`${styles.folder_explorer_line_wrapper} ${
        element.is_folder ? styles.folder : ""
      }`}
      onClick={() => {
        if (element.is_folder) {
          setCurrentFolder({
            ...element,
            parentKMSElement: element.parentKMSElement,
          });
        }
      }}
      draggable
      onDragStart={(event) => onDragStart && onDragStart(event, element)}
      onDrop={(event) => onDrop && onDrop(event, element)}
      onDragOver={onDragOver}
    >
      <div className={styles.left}>
        <div className={styles.checkbox}>
          {onDragStart && (
            <Checkbox
              checked={selectedKnowledges.includes(element)}
              setChecked={(checked) => handleCheckboxChange(checked)}
            />
          )}
        </div>
        <Icon
          name={
            element.is_folder
              ? "folder"
              : fileType !== "default"
              ? iconList[fileType.toLocaleLowerCase()]
                ? fileType.toLowerCase()
                : "file"
              : "file"
          }
          size="small"
          customColor={getIconColor()}
          color={element.is_folder ? "black" : undefined}
        />
        <span className={styles.name}>{element.file_name}</span>
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
