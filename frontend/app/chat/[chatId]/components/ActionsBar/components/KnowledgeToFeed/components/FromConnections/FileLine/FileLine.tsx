import { useState } from "react";

import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import Icon from "@/lib/components/ui/Icon/Icon";

import styles from "./FileLine.module.scss";

import { useFromConnectionsContext } from "../FromConnectionsProvider/hooks/useFromConnectionContext";

interface FileLineProps {
  name: string;
  selectable: boolean;
  id: string;
}

export const FileLine = ({
  name,
  selectable,
  id,
}: FileLineProps): JSX.Element => {
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
    <div className={styles.file_line_wrapper}>
      {selectable && (
        <Checkbox checked={checked} setChecked={() => handleSetChecked()} />
      )}
      <Icon name="file" color="black" size="small" />
      <span className={styles.file_name}>{name}</span>
    </div>
  );
};
