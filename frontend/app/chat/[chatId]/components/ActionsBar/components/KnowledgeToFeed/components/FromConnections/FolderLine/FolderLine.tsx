import { SyncElementLine } from "../SyncElementLine/SyncElementLine";

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
  return (
    <SyncElementLine
      name={name}
      selectable={selectable}
      id={id}
      isFolder={true}
    />
  );
};
