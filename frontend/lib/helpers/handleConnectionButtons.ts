import { SetStateAction } from "react";

import { OpenedConnection } from "../api/sync/types";

const isRemoveAll = (
  matchingOpenedConnection: OpenedConnection,
  currentConnection: OpenedConnection | undefined
): boolean => {
  return !!(
    currentConnection?.submitted &&
    matchingOpenedConnection.selectedFiles.files.length === 0 &&
    !currentConnection.cleaned
  );
};

const arraysAreEqual = (arr1: string[], arr2: string[]): boolean => {
  if (arr1.length !== arr2.length) {
    return false;
  }

  for (let i = 0; i < arr1.length; i++) {
    if (arr1[i] !== arr2[i]) {
      return false;
    }
  }

  return true;
};

export const handleGetButtonProps = (
  currentConnection: OpenedConnection | undefined,
  openedConnections: OpenedConnection[],
  setOpenedConnections: React.Dispatch<
    React.SetStateAction<OpenedConnection[]>
  >,
  currentSyncId: number | undefined,
  setCurrentSyncId: React.Dispatch<React.SetStateAction<number | undefined>>
): {
  label: string;
  type: "dangerous" | "primary";
  disabled: boolean;
  callback: () => void;
} => {
  const matchingOpenedConnection =
    currentConnection &&
    openedConnections.find(
      (conn) => conn.user_sync_id === currentConnection.user_sync_id
    );

  if (matchingOpenedConnection) {
    if (isRemoveAll(matchingOpenedConnection, currentConnection)) {
      return {
        label: "Remove All",
        type: "dangerous",
        disabled: false,
        callback: () =>
          removeConnection(
            setOpenedConnections,
            currentSyncId,
            setCurrentSyncId
          ),
      };
    } else if (currentConnection.submitted) {
      const matchingSelectedFileIds =
        matchingOpenedConnection.selectedFiles.files
          .map((file) => file.id)
          .sort();

      const currentSelectedFileIds = currentConnection.selectedFiles.files
        .map((file) => file.id)
        .sort();

      const isDisabled = arraysAreEqual(
        matchingSelectedFileIds,
        currentSelectedFileIds
      );

      return {
        label: "Update added files",
        type: "primary",
        disabled:
          !matchingOpenedConnection.selectedFiles.files.length || isDisabled,
        callback: () =>
          addConnection(setOpenedConnections, currentSyncId, setCurrentSyncId),
      };
    }
  }

  return {
    label: "Add specific files",
    type: "primary",
    disabled: !matchingOpenedConnection?.selectedFiles.files.length,
    callback: () =>
      addConnection(setOpenedConnections, currentSyncId, setCurrentSyncId),
  };
};

const addConnection = (
  setOpenedConnections: React.Dispatch<
    React.SetStateAction<OpenedConnection[]>
  >,
  currentSyncId: number | undefined,
  setCurrentSyncId: React.Dispatch<React.SetStateAction<number | undefined>>
): void => {
  setOpenedConnections((prevConnections) => {
    const connectionIndex = prevConnections.findIndex(
      (connection) => connection.user_sync_id === currentSyncId
    );

    if (connectionIndex !== -1) {
      const newConnections = [...prevConnections];
      newConnections[connectionIndex] = {
        ...newConnections[connectionIndex],
        submitted: true,
        cleaned: false,
      };

      return newConnections;
    }

    return prevConnections;
  });

  setCurrentSyncId(undefined);
};

const removeConnection = (
  setOpenedConnections: React.Dispatch<
    React.SetStateAction<OpenedConnection[]>
  >,
  currentSyncId: number | undefined,
  setCurrentSyncId: React.Dispatch<React.SetStateAction<number | undefined>>
): void => {
  setOpenedConnections((prevConnections) =>
    prevConnections
      .filter((connection) => {
        return (
          connection.user_sync_id === currentSyncId || !!connection.last_synced
        );
      })
      .map((connection) => {
        if (
          connection.user_sync_id === currentSyncId &&
          !!connection.last_synced
        ) {
          return { ...connection, cleaned: true };
        } else {
          return connection;
        }
      })
  );

  setCurrentSyncId(undefined);
};

export const createHandleGetButtonProps =
  (
    currentConnection: OpenedConnection | undefined,
    openedConnections: OpenedConnection[],
    setOpenedConnections: {
      (value: SetStateAction<OpenedConnection[]>): void;
      (value: SetStateAction<OpenedConnection[]>): void;
    },
    currentSyncId: number | undefined,
    setCurrentSyncId: {
      (value: SetStateAction<number | undefined>): void;
      (value: SetStateAction<number | undefined>): void;
    }
  ) =>
  (): {
    label: string;
    type: "primary" | "dangerous";
    disabled: boolean;
    callback: () => void;
  } =>
    handleGetButtonProps(
      currentConnection,
      openedConnections,
      setOpenedConnections,
      currentSyncId,
      setCurrentSyncId
    );
