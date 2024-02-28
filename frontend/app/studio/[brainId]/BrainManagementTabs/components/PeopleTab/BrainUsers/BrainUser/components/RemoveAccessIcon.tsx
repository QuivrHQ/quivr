import { MdOutlineRemoveCircle, MdOutlineTimelapse } from "react-icons/md";

type RemoveAccessIconProps = {
  onClick: () => void;
  isRemovingAccess: boolean;
};
export const RemoveAccessIcon = ({
  onClick,
  isRemovingAccess,
}: RemoveAccessIconProps): JSX.Element => {
  return isRemovingAccess ? (
    <div className="animate-pulse">
      <MdOutlineTimelapse />
    </div>
  ) : (
    <div className="cursor-pointer" onClick={onClick}>
      <MdOutlineRemoveCircle />
    </div>
  );
};
