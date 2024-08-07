import { SyncElementLine } from "../SyncElementLine/SyncElementLine";

interface FolderLineProps {
  name: string;
  selectable: boolean;
  id: string;
  icon?: string;
}

export const FolderLine = ({
  name,
  selectable,
  id,
  icon
}: FolderLineProps): JSX.Element => {
  return (
    <SyncElementLine
      name={name}
      selectable={selectable}
      id={id}
      isFolder={true}
      icon= {icon}
    />
  );
};
