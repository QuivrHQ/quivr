import { MdRemoveCircleOutline } from "react-icons/md";

type MentionItemProps = {
  text: string;
  onRemove: () => void;
  prefix?: string;
};

export const MentionItem = ({
  text,
  prefix = "",
  onRemove,
}: MentionItemProps): JSX.Element => {
  return (
    <div className="relative">
      <div className="flex items-center bg-gray-300 mr-2 text-gray-600 rounded-2xl py-1 px-2">
        <span className="flex-grow">{`${prefix}${text}`}</span>
        <MdRemoveCircleOutline
          className="cursor-pointer absolute top-[-10px] right-[5px]"
          onClick={onRemove}
        />
      </div>
    </div>
  );
};
