import { useState } from "react";

import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./FolderLine.module.scss";

import { useFromConnectionsContext } from "../FromConnectionsProvider/hooks/useFromConnectionContext";

interface FolderLineProps {
  name: string;
  selectable: boolean;
  id: string;
}

export const FolderLine = ({
  name,
  selectable,
  id,
}: FolderLineProps): JSX.Element => {
  const [isCheckboxHovered, setIsCheckboxHovered] = useState(false);
  const { currentSyncId, openedConnections, setOpenedConnections } =
    useFromConnectionsContext();

  const initialChecked = (): boolean => {
    const currentConnection = openedConnections.find(
      (connection) => connection.id === currentSyncId
    );

    return currentConnection
      ? currentConnection.selectedFiles.includes(id)
      : false;
  };

  const [checked] = useState<boolean>(initialChecked);

  const handleSetChecked = () => {
    setOpenedConnections((prevState) => {
      return prevState.map((connection) => {
        if (connection.id === currentSyncId) {
          if (connection.selectedFiles.includes(id)) {
            return {
              ...connection,
              selectedFiles: connection.selectedFiles.filter(
                (fileId) => fileId !== id
              ),
            };
          } else {
            return {
              ...connection,
              selectedFiles: [...connection.selectedFiles, id],
            };
          }
        } else {
          return connection;
        }
      });
    });
  };

  return (
    <div
      className={`${styles.folder_line_wrapper} ${
        isCheckboxHovered ? styles.no_hover : ""
      }`}
    >
      {selectable && (
        <div
          className={styles.checkbox_wrapper}
          onMouseEnter={() => setIsCheckboxHovered(true)}
          onMouseLeave={() => setIsCheckboxHovered(false)}
        >
          <Checkbox checked={checked} setChecked={() => handleSetChecked()} />
        </div>
      )}
      <Icon name="folder" color="black" size="normal" />
      <span className={styles.folder_name}>{name}</span>
    </div>
  );
};
