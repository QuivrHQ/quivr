import { useState } from "react";

import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import Tooltip from "@/lib/components/ui/Tooltip/Tooltip";

import styles from "./SyncElementLine.module.scss";

import { useFromConnectionsContext } from "../FromConnectionsProvider/hooks/useFromConnectionContext";

interface SyncElementLineProps {
  name: string;
  selectable: boolean;
  id: string;
  isFolder: boolean;
}

export const SyncElementLine = ({
  name,
  selectable,
  id,
  isFolder,
}: SyncElementLineProps): JSX.Element => {
  const [isCheckboxHovered, setIsCheckboxHovered] = useState(false);
  const { currentSyncId, openedConnections, setOpenedConnections } =
    useFromConnectionsContext();

  const initialChecked = (): boolean => {
    const currentConnection = openedConnections.find(
      (connection) => connection.user_sync_id === currentSyncId
    );

    return currentConnection
      ? currentConnection.selectedFiles.files.some((file) => file.id === id)
      : false;
  };

  const [checked, setChecked] = useState<boolean>(initialChecked);

  const handleSetChecked = () => {
    setOpenedConnections((prevState) => {
      return prevState.map((connection) => {
        if (connection.user_sync_id === currentSyncId) {
          const isFileSelected = connection.selectedFiles.files.some(
            (file) => file.id === id
          );
          const updatedFiles = isFileSelected
            ? connection.selectedFiles.files.filter((file) => file.id !== id)
            : [
                ...connection.selectedFiles.files,
                { id, name, is_folder: isFolder },
              ];

          return {
            ...connection,
            selectedFiles: {
              files: updatedFiles,
            },
          };
        }

        return connection;
      });
    });
    setChecked((prevChecked) => !prevChecked);
  };

  const content = (
    <div
      className={`${styles.sync_element_line_wrapper} ${
        isCheckboxHovered || !isFolder || checked ? styles.no_hover : ""
      }`}
      onClick={(event) => {
        if (isFolder && checked) {
          event.stopPropagation();
        }
      }}
    >
      <div className={`${styles.left} ${isFolder ? styles.folder : ""}`}>
        {!isFolder && (
          <div
            onMouseEnter={() => setIsCheckboxHovered(true)}
            onMouseLeave={() => setIsCheckboxHovered(false)}
            style={{ pointerEvents: "auto" }}
          >
            <Checkbox
              checked={checked}
              setChecked={handleSetChecked}
              disabled={!selectable}
            />
          </div>
        )}

        <Icon name={isFolder ? "folder" : "file"} color="black" size="normal" />
        <span className={styles.element_name}>{name}</span>
      </div>

      {isFolder && (
        <Icon
          name="chevronRight"
          color="black"
          size="normal"
          handleHover={true}
        />
      )}
    </div>
  );

  return selectable ? (
    content
  ) : (
    <Tooltip tooltip="Only premium members can sync folders. This feature automatically adds new files from your folders to your brain, keeping it up-to-date without manual effort.">
      {content}
    </Tooltip>
  );
};
