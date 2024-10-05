import { SyncElementLine } from "../SyncElementLine/SyncElementLine";

interface FileLineProps {
  name: string;
  selectable: boolean;
  id: string;
  icon?: string;
}

export const FileLine = ({
  name,
  selectable,
  id,
  icon,
}: FileLineProps): JSX.Element => {
  return (
    <SyncElementLine
      name={name}
      selectable={selectable}
      id={id}
      isFolder={false}
      icon={icon}
    />
  );
};
