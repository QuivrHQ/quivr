import { SyncElementLine } from "../SyncElementLine/SyncElementLine";

interface FolderLineProps {
  name: string;
  selectable: boolean;
  id: string;
  icon?: string;
  isAlsoFile?: boolean;
}

export const FolderLine = ({
  name,
  selectable,
  id,
  icon,
  isAlsoFile,
}: FolderLineProps): JSX.Element => {
  return (
    <SyncElementLine
      name={name}
      selectable={selectable}
      id={id}
      isFolder={true}
      isAlsoFile={isAlsoFile}
      icon={icon}
    />
  );
};
