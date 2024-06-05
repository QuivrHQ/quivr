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
      ? currentConnection.selectedFiles.files.some((file) => file.id === id)
      : false;
  };

  const [checked] = useState<boolean>(initialChecked);

  const handleSetChecked = () => {
    setOpenedConnections((prevState) => {
      return prevState.map((connection) => {
        if (connection.id === currentSyncId) {
          const currentConnection = prevState.find(
            (conn) => conn.id === currentSyncId
          );

          if (
            currentConnection?.selectedFiles.files.some(
              (file) => file.id === id
            )
          ) {
            return {
              ...connection,
              selectedFiles: {
                files: connection.selectedFiles.files.filter(
                  (file) => file.id !== id
                ),
              },
            };
          } else {
            return {
              ...connection,
              selectedFiles: {
                files: [
                  ...connection.selectedFiles.files,
                  { id, name, is_folder: true },
                ],
              },
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
